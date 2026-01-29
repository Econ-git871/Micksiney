/**
 * Core types for table to shapes conversion
 */

/** RGB color representation */
export interface RgbColor {
  r: number;
  g: number;
  b: number;
}

/** Border style information */
export interface BorderStyle {
  color: string;
  weight: number;
  style: 'solid' | 'dashed' | 'dotted' | 'none';
}

/** Cell border information (all four sides) */
export interface CellBorders {
  top: BorderStyle;
  right: BorderStyle;
  bottom: BorderStyle;
  left: BorderStyle;
}

/** Text formatting information */
export interface TextFormat {
  fontFamily: string;
  fontSize: number;
  fontColor: string;
  bold: boolean;
  italic: boolean;
  underline: boolean;
  horizontalAlignment: 'left' | 'center' | 'right';
  verticalAlignment: 'top' | 'middle' | 'bottom';
}

/** Cell data extracted from table */
export interface CellData {
  row: number;
  column: number;
  rowSpan: number;
  columnSpan: number;
  text: string;
  textFormat: TextFormat;
  backgroundColor: string;
  borders: CellBorders;
  width: number;
  height: number;
  x: number;
  y: number;
}

/** Table data extracted from PowerPoint */
export interface TableData {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  rowCount: number;
  columnCount: number;
  cells: CellData[];
  columnWidths: number[];
  rowHeights: number[];
}

/** Conversion options */
export interface ConversionOptions {
  keepBorder: boolean;
  keepBackground: boolean;
  keepText: boolean;
  keepTextFormat: boolean;
  deleteOriginal: boolean;
}

/** Conversion result */
export interface ConversionResult {
  success: boolean;
  shapesCreated: number;
  message: string;
  error?: string;
}

/** Progress callback type */
export type ProgressCallback = (progress: number, message: string) => void;
