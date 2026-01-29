/**
 * Shape Creator Module
 * Creates PowerPoint shapes from table cell data
 */

import {
  CellData,
  ConversionOptions,
  ProgressCallback,
} from './types';

/**
 * Create a rectangle shape for a table cell
 */
export async function createCellShape(
  cell: CellData,
  options: ConversionOptions
): Promise<void> {
  return new Promise((resolve, reject) => {
    PowerPoint.run(async (context) => {
      try {
        const slide = context.presentation.getSelectedSlides().getItemAt(0);

        // Create rectangle shape
        const shape = slide.shapes.addGeometricShape(
          PowerPoint.GeometricShapeType.rectangle,
          {
            left: cell.x,
            top: cell.y,
            width: cell.width,
            height: cell.height,
          }
        );

        // Apply fill color
        if (options.keepBackground) {
          const fill = shape.fill;
          fill.setSolidColor(cell.backgroundColor);
        } else {
          shape.fill.setSolidColor('#FFFFFF');
        }

        // Apply border/line
        if (options.keepBorder) {
          const line = shape.lineFormat;
          line.color = cell.borders.top.color;
          line.weight = cell.borders.top.weight;
        } else {
          // Set minimal border
          const line = shape.lineFormat;
          line.color = '#D0D0D0';
          line.weight = 0.5;
        }

        await context.sync();

        // Add text if option is enabled and cell has text
        if (options.keepText && cell.text && cell.text.trim()) {
          const textFrame = shape.textFrame;

          // Set text
          const textRange = textFrame.textRange;
          textRange.text = cell.text.trim();

          // Apply text formatting if option is enabled
          if (options.keepTextFormat) {
            const font = textRange.font;
            font.name = cell.textFormat.fontFamily;
            font.size = cell.textFormat.fontSize;
            font.color = cell.textFormat.fontColor;
            font.bold = cell.textFormat.bold;
            font.italic = cell.textFormat.italic;

            if (cell.textFormat.underline) {
              font.underline = PowerPoint.TextUnderlineType.single;
            }

            // Set paragraph alignment
            const paragraph = textRange.paragraphFormat;
            paragraph.horizontalAlignment = mapAlignment(cell.textFormat.horizontalAlignment);
          }

          // Set vertical alignment
          textFrame.verticalAlignment = mapVerticalAlignment(cell.textFormat.verticalAlignment);

          // Set text margins
          textFrame.leftMargin = 5;
          textFrame.rightMargin = 5;
          textFrame.topMargin = 3;
          textFrame.bottomMargin = 3;

          // Auto-fit settings
          textFrame.autoSizeSetting = PowerPoint.ShapeAutoSize.autoSizeNone;
        }

        await context.sync();
        resolve();
      } catch (error) {
        console.error('Error creating cell shape:', error);
        reject(error);
      }
    });
  });
}

/**
 * Create all shapes for a table
 */
export async function createShapesFromCells(
  cells: CellData[],
  options: ConversionOptions,
  onProgress?: ProgressCallback
): Promise<number> {
  let shapesCreated = 0;
  const totalCells = cells.length;

  for (let i = 0; i < cells.length; i++) {
    const cell = cells[i];

    try {
      await createCellShape(cell, options);
      shapesCreated++;

      if (onProgress) {
        const progress = Math.round(((i + 1) / totalCells) * 100);
        onProgress(progress, `正在创建形状 ${i + 1}/${totalCells}`);
      }
    } catch (error) {
      console.error(`Error creating shape for cell [${cell.row}, ${cell.column}]:`, error);
    }
  }

  return shapesCreated;
}

/**
 * Map horizontal alignment to PowerPoint enum
 */
function mapAlignment(
  alignment: 'left' | 'center' | 'right'
): PowerPoint.ParagraphHorizontalAlignment {
  switch (alignment) {
    case 'left':
      return PowerPoint.ParagraphHorizontalAlignment.left;
    case 'right':
      return PowerPoint.ParagraphHorizontalAlignment.right;
    case 'center':
    default:
      return PowerPoint.ParagraphHorizontalAlignment.center;
  }
}

/**
 * Map vertical alignment to PowerPoint enum
 */
function mapVerticalAlignment(
  alignment: 'top' | 'middle' | 'bottom'
): PowerPoint.TextVerticalAlignment {
  switch (alignment) {
    case 'top':
      return PowerPoint.TextVerticalAlignment.top;
    case 'bottom':
      return PowerPoint.TextVerticalAlignment.bottom;
    case 'middle':
    default:
      return PowerPoint.TextVerticalAlignment.middle;
  }
}

/**
 * Batch create shapes for better performance
 */
export async function createShapesBatch(
  cells: CellData[],
  options: ConversionOptions,
  onProgress?: ProgressCallback
): Promise<number> {
  return new Promise((resolve) => {
    PowerPoint.run(async (context) => {
      try {
        const slide = context.presentation.getSelectedSlides().getItemAt(0);
        const totalCells = cells.length;
        let shapesCreated = 0;

        // Create all shapes in a single context
        for (let i = 0; i < cells.length; i++) {
          const cell = cells[i];

          // Create rectangle shape
          const shape = slide.shapes.addGeometricShape(
            PowerPoint.GeometricShapeType.rectangle,
            {
              left: cell.x,
              top: cell.y,
              width: cell.width,
              height: cell.height,
            }
          );

          // Apply fill color
          if (options.keepBackground) {
            shape.fill.setSolidColor(cell.backgroundColor);
          } else {
            shape.fill.setSolidColor('#FFFFFF');
          }

          // Apply border
          if (options.keepBorder) {
            shape.lineFormat.color = cell.borders.top.color;
            shape.lineFormat.weight = cell.borders.top.weight;
          } else {
            shape.lineFormat.color = '#D0D0D0';
            shape.lineFormat.weight = 0.5;
          }

          shapesCreated++;
        }

        // Sync to create all shapes
        await context.sync();

        if (onProgress) {
          onProgress(50, '形状已创建，正在添加文本...');
        }

        // Now add text to shapes that have content
        const shapes = slide.shapes;
        shapes.load('items');
        await context.sync();

        // Get the newly created shapes (last N shapes)
        const newShapes = shapes.items.slice(-cells.length);

        for (let i = 0; i < cells.length; i++) {
          const cell = cells[i];
          const shape = newShapes[i];

          if (options.keepText && cell.text && cell.text.trim()) {
            const textFrame = shape.textFrame;
            const textRange = textFrame.textRange;
            textRange.text = cell.text.trim();

            if (options.keepTextFormat) {
              const font = textRange.font;
              font.name = cell.textFormat.fontFamily;
              font.size = cell.textFormat.fontSize;
              font.color = cell.textFormat.fontColor;
              font.bold = cell.textFormat.bold;
              font.italic = cell.textFormat.italic;

              if (cell.textFormat.underline) {
                font.underline = PowerPoint.TextUnderlineType.single;
              }

              textRange.paragraphFormat.horizontalAlignment = mapAlignment(
                cell.textFormat.horizontalAlignment
              );
            }

            textFrame.verticalAlignment = mapVerticalAlignment(
              cell.textFormat.verticalAlignment
            );
            textFrame.leftMargin = 5;
            textFrame.rightMargin = 5;
            textFrame.topMargin = 3;
            textFrame.bottomMargin = 3;
          }

          if (onProgress) {
            const progress = 50 + Math.round(((i + 1) / totalCells) * 50);
            onProgress(progress, `正在设置文本 ${i + 1}/${totalCells}`);
          }
        }

        await context.sync();

        if (onProgress) {
          onProgress(100, '转换完成');
        }

        resolve(shapesCreated);
      } catch (error) {
        console.error('Error in batch shape creation:', error);
        resolve(0);
      }
    });
  });
}
