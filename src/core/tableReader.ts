/**
 * Table Reader Module
 * Extracts table data from PowerPoint slides
 */

import {
  TableData,
  CellData,
  CellBorders,
  BorderStyle,
  TextFormat,
} from './types';

/** Default border style */
const defaultBorder: BorderStyle = {
  color: '#000000',
  weight: 1,
  style: 'solid',
};

/** Default text format */
const defaultTextFormat: TextFormat = {
  fontFamily: 'Calibri',
  fontSize: 11,
  fontColor: '#000000',
  bold: false,
  italic: false,
  underline: false,
  horizontalAlignment: 'center',
  verticalAlignment: 'middle',
};

/**
 * Check if the selected shape is a table
 */
export async function isTableSelected(): Promise<boolean> {
  return new Promise((resolve) => {
    PowerPoint.run(async (context) => {
      try {
        const selection = context.presentation.getSelectedShapes();
        selection.load('items');
        await context.sync();

        if (selection.items.length !== 1) {
          resolve(false);
          return;
        }

        const shape = selection.items[0];
        shape.load('type');
        await context.sync();

        // Check if it's a table (type value for table)
        resolve(shape.type === PowerPoint.ShapeType.table);
      } catch (error) {
        console.error('Error checking table selection:', error);
        resolve(false);
      }
    });
  });
}

/**
 * Get the selected table shape
 */
export async function getSelectedTable(): Promise<PowerPoint.Shape | null> {
  return new Promise((resolve) => {
    PowerPoint.run(async (context) => {
      try {
        const selection = context.presentation.getSelectedShapes();
        selection.load('items');
        await context.sync();

        if (selection.items.length !== 1) {
          resolve(null);
          return;
        }

        const shape = selection.items[0];
        shape.load(['type', 'id', 'left', 'top', 'width', 'height']);
        await context.sync();

        if (shape.type === PowerPoint.ShapeType.table) {
          resolve(shape);
        } else {
          resolve(null);
        }
      } catch (error) {
        console.error('Error getting selected table:', error);
        resolve(null);
      }
    });
  });
}

/**
 * Extract complete table data from a PowerPoint table
 */
export async function extractTableData(): Promise<TableData | null> {
  return new Promise((resolve) => {
    PowerPoint.run(async (context) => {
      try {
        const selection = context.presentation.getSelectedShapes();
        selection.load('items');
        await context.sync();

        if (selection.items.length !== 1) {
          resolve(null);
          return;
        }

        const shape = selection.items[0];
        shape.load(['type', 'id', 'left', 'top', 'width', 'height']);
        await context.sync();

        if (shape.type !== PowerPoint.ShapeType.table) {
          resolve(null);
          return;
        }

        // Get table reference (use type assertion as table property may not be in type definitions)
        const table = (shape as any).table;
        if (!table) {
          resolve(null);
          return;
        }
        table.load(['rowCount', 'columnCount']);
        await context.sync();

        const rowCount = table.rowCount;
        const columnCount = table.columnCount;

        // Calculate uniform cell dimensions
        const cellWidth = shape.width / columnCount;
        const cellHeight = shape.height / rowCount;

        // Create arrays for column widths and row heights
        const columnWidths: number[] = Array(columnCount).fill(cellWidth);
        const rowHeights: number[] = Array(rowCount).fill(cellHeight);

        // Extract cell data
        const cells: CellData[] = [];
        const processedCells = new Set<string>();

        for (let row = 0; row < rowCount; row++) {
          for (let col = 0; col < columnCount; col++) {
            const cellKey = `${row}-${col}`;
            if (processedCells.has(cellKey)) {
              continue;
            }

            const cell = table.getCell(row, col);
            cell.load(['rowIndex', 'columnIndex']);

            // Load text frame for cell content
            const textFrame = cell.textFrame;
            textFrame.load(['textRange', 'hasText']);

            await context.sync();

            // Get cell text
            let cellText = '';
            let textFormat = { ...defaultTextFormat };

            if (textFrame.hasText) {
              const textRange = textFrame.textRange;
              textRange.load(['text']);

              // Try to load font properties
              const font = textRange.font;
              font.load(['name', 'size', 'color', 'bold', 'italic', 'underline']);

              // Load paragraph alignment
              const paragraph = textRange.paragraphFormat;
              paragraph.load(['horizontalAlignment']);

              await context.sync();

              cellText = textRange.text || '';

              // Extract text formatting
              // Check underline using string comparison as TextUnderlineType may not be available
              const isUnderlined = font.underline && (font.underline as any) !== 'None';
              textFormat = {
                fontFamily: font.name || defaultTextFormat.fontFamily,
                fontSize: font.size || defaultTextFormat.fontSize,
                fontColor: font.color || defaultTextFormat.fontColor,
                bold: font.bold || false,
                italic: font.italic || false,
                underline: isUnderlined,
                horizontalAlignment: mapHorizontalAlignment(paragraph.horizontalAlignment),
                verticalAlignment: 'middle',
              };
            }

            // Get fill color
            const fill = cell.fill;
            fill.load(['solidColor']);
            await context.sync();

            const backgroundColor = fill.solidColor?.color || '#FFFFFF';

            // Determine cell span (simplified - PowerPoint API has limited merge cell support)
            const rowSpan = 1;
            const columnSpan = 1;

            // Calculate cell position
            const x = shape.left + col * cellWidth;
            const y = shape.top + row * cellHeight;

            const cellData: CellData = {
              row,
              column: col,
              rowSpan,
              columnSpan,
              text: cellText,
              textFormat,
              backgroundColor,
              borders: getDefaultBorders(),
              width: cellWidth * columnSpan,
              height: cellHeight * rowSpan,
              x,
              y,
            };

            cells.push(cellData);

            // Mark cells as processed (for merged cells)
            for (let r = row; r < row + rowSpan; r++) {
              for (let c = col; c < col + columnSpan; c++) {
                processedCells.add(`${r}-${c}`);
              }
            }
          }
        }

        const tableData: TableData = {
          id: shape.id,
          x: shape.left,
          y: shape.top,
          width: shape.width,
          height: shape.height,
          rowCount,
          columnCount,
          cells,
          columnWidths,
          rowHeights,
        };

        resolve(tableData);
      } catch (error) {
        console.error('Error extracting table data:', error);
        resolve(null);
      }
    });
  });
}

/**
 * Map PowerPoint horizontal alignment to our type
 */
function mapHorizontalAlignment(
  alignment: PowerPoint.ParagraphHorizontalAlignment | undefined
): 'left' | 'center' | 'right' {
  switch (alignment) {
    case PowerPoint.ParagraphHorizontalAlignment.left:
      return 'left';
    case PowerPoint.ParagraphHorizontalAlignment.right:
      return 'right';
    case PowerPoint.ParagraphHorizontalAlignment.center:
    default:
      return 'center';
  }
}

/**
 * Get default borders for a cell
 */
function getDefaultBorders(): CellBorders {
  return {
    top: { ...defaultBorder },
    right: { ...defaultBorder },
    bottom: { ...defaultBorder },
    left: { ...defaultBorder },
  };
}

/**
 * Delete the original table after conversion
 */
export async function deleteTable(tableId: string): Promise<boolean> {
  return new Promise((resolve) => {
    PowerPoint.run(async (context) => {
      try {
        const slide = context.presentation.getSelectedSlides().getItemAt(0);
        const shapes = slide.shapes;
        shapes.load('items');
        await context.sync();

        for (const shape of shapes.items) {
          shape.load('id');
        }
        await context.sync();

        for (const shape of shapes.items) {
          if (shape.id === tableId) {
            shape.delete();
            await context.sync();
            resolve(true);
            return;
          }
        }

        resolve(false);
      } catch (error) {
        console.error('Error deleting table:', error);
        resolve(false);
      }
    });
  });
}
