/**
 * Table to Shapes Converter
 * Main conversion logic combining table reading and shape creation
 */

import {
  ConversionOptions,
  ConversionResult,
  ProgressCallback,
} from './types';
import { extractTableData, deleteTable, isTableSelected } from './tableReader';
import { createShapesBatch } from './shapeCreator';

/**
 * Convert the selected table to shapes
 */
export async function convertTableToShapes(
  options: ConversionOptions,
  onProgress?: ProgressCallback
): Promise<ConversionResult> {
  try {
    // Check if a table is selected
    if (onProgress) {
      onProgress(5, '正在检查选择...');
    }

    const isTable = await isTableSelected();
    if (!isTable) {
      return {
        success: false,
        shapesCreated: 0,
        message: '请先选择一个表格',
        error: 'NO_TABLE_SELECTED',
      };
    }

    // Extract table data
    if (onProgress) {
      onProgress(10, '正在读取表格数据...');
    }

    const tableData = await extractTableData();
    if (!tableData) {
      return {
        success: false,
        shapesCreated: 0,
        message: '无法读取表格数据',
        error: 'TABLE_READ_ERROR',
      };
    }

    if (onProgress) {
      onProgress(20, `已读取 ${tableData.cells.length} 个单元格`);
    }

    // Store table ID for later deletion
    const tableId = tableData.id;

    // Create shapes from cells
    if (onProgress) {
      onProgress(25, '正在创建形状...');
    }

    const progressWrapper: ProgressCallback = (progress, message) => {
      // Map 0-100 to 25-90
      const mappedProgress = 25 + Math.round(progress * 0.65);
      if (onProgress) {
        onProgress(mappedProgress, message);
      }
    };

    const shapesCreated = await createShapesBatch(
      tableData.cells,
      options,
      progressWrapper
    );

    if (shapesCreated === 0) {
      return {
        success: false,
        shapesCreated: 0,
        message: '创建形状失败',
        error: 'SHAPE_CREATION_ERROR',
      };
    }

    // Delete original table if option is enabled
    if (options.deleteOriginal) {
      if (onProgress) {
        onProgress(95, '正在删除原表格...');
      }

      await deleteTable(tableId);
    }

    if (onProgress) {
      onProgress(100, '转换完成');
    }

    return {
      success: true,
      shapesCreated,
      message: `成功创建 ${shapesCreated} 个形状`,
    };
  } catch (error) {
    console.error('Conversion error:', error);
    return {
      success: false,
      shapesCreated: 0,
      message: '转换过程中发生错误',
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

/**
 * Check if the current selection is a valid table
 */
export async function checkTableSelection(): Promise<{
  isValid: boolean;
  message: string;
}> {
  try {
    const isTable = await isTableSelected();

    if (isTable) {
      const tableData = await extractTableData();
      if (tableData) {
        return {
          isValid: true,
          message: `已选择表格：${tableData.rowCount} 行 × ${tableData.columnCount} 列`,
        };
      }
    }

    return {
      isValid: false,
      message: '请选择一个表格',
    };
  } catch (error) {
    return {
      isValid: false,
      message: '检查选择时发生错误',
    };
  }
}
