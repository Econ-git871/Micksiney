using System;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.TableTools
{
    public static class TableToShapesHelper
    {
        /// <summary>
        /// Convert selected table to individual text box shapes
        /// </summary>
        public static void ConvertTableToShapes()
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            var slide = Globals.ThisAddIn.ActiveSlide;

            if (shapes == null || shapes.Count != 1 || slide == null)
            {
                MessageBox.Show("Please select exactly one table.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            var shape = shapes[1];
            if (!shape.HasTable)
            {
                MessageBox.Show("Selected shape is not a table.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var table = shape.Table;
                float tableLeft = shape.Left;
                float tableTop = shape.Top;

                int rowCount = table.Rows.Count;
                int colCount = table.Columns.Count;

                // Calculate cell positions
                float[] columnLefts = new float[colCount + 1];
                float[] rowTops = new float[rowCount + 1];

                columnLefts[0] = tableLeft;
                for (int c = 1; c <= colCount; c++)
                {
                    columnLefts[c] = columnLefts[c - 1] + table.Columns[c].Width;
                }

                rowTops[0] = tableTop;
                for (int r = 1; r <= rowCount; r++)
                {
                    rowTops[r] = rowTops[r - 1] + table.Rows[r].Height;
                }

                // Track merged cells to avoid duplicates
                bool[,] processed = new bool[rowCount + 1, colCount + 1];

                // Create text boxes for each cell
                for (int r = 1; r <= rowCount; r++)
                {
                    for (int c = 1; c <= colCount; c++)
                    {
                        if (processed[r, c]) continue;

                        var cell = table.Cell(r, c);

                        // Check for merged cells
                        int rowSpan = 1;
                        int colSpan = 1;

                        // Detect horizontal merge
                        try
                        {
                            while (c + colSpan <= colCount && cell.Merge(table.Cell(r, c + colSpan)))
                            {
                                colSpan++;
                            }
                        }
                        catch { }

                        // Detect vertical merge
                        try
                        {
                            while (r + rowSpan <= rowCount && cell.Merge(table.Cell(r + rowSpan, c)))
                            {
                                rowSpan++;
                            }
                        }
                        catch { }

                        // Mark cells as processed
                        for (int dr = 0; dr < rowSpan; dr++)
                        {
                            for (int dc = 0; dc < colSpan; dc++)
                            {
                                if (r + dr <= rowCount && c + dc <= colCount)
                                {
                                    processed[r + dr, c + dc] = true;
                                }
                            }
                        }

                        // Calculate cell dimensions
                        float cellLeft = columnLefts[c - 1];
                        float cellTop = rowTops[r - 1];
                        float cellWidth = columnLefts[c - 1 + colSpan] - cellLeft;
                        float cellHeight = rowTops[r - 1 + rowSpan] - cellTop;

                        // Create text box
                        var textBox = slide.Shapes.AddTextbox(
                            Office.MsoTextOrientation.msoTextOrientationHorizontal,
                            cellLeft, cellTop, cellWidth, cellHeight);

                        // Copy cell content
                        if (cell.Shape.HasTextFrame == Office.MsoTriState.msoTrue)
                        {
                            string text = cell.Shape.TextFrame.TextRange.Text;
                            textBox.TextFrame.TextRange.Text = text;

                            // Copy text formatting
                            try
                            {
                                var srcFont = cell.Shape.TextFrame.TextRange.Font;
                                var dstFont = textBox.TextFrame.TextRange.Font;
                                dstFont.Name = srcFont.Name;
                                dstFont.Size = srcFont.Size;
                                dstFont.Color.RGB = srcFont.Color.RGB;
                                dstFont.Bold = srcFont.Bold;
                                dstFont.Italic = srcFont.Italic;
                                dstFont.Underline = srcFont.Underline;
                            }
                            catch { }

                            // Copy paragraph formatting
                            try
                            {
                                var srcPara = cell.Shape.TextFrame.TextRange.ParagraphFormat;
                                var dstPara = textBox.TextFrame.TextRange.ParagraphFormat;
                                dstPara.Alignment = srcPara.Alignment;
                            }
                            catch { }
                        }

                        // Copy cell background color
                        try
                        {
                            if (cell.Shape.Fill.Type == Office.MsoFillType.msoFillSolid)
                            {
                                textBox.Fill.Solid();
                                textBox.Fill.ForeColor.RGB = cell.Shape.Fill.ForeColor.RGB;
                            }
                            else
                            {
                                textBox.Fill.Visible = Office.MsoTriState.msoFalse;
                            }
                        }
                        catch
                        {
                            textBox.Fill.Visible = Office.MsoTriState.msoFalse;
                        }

                        // Set border
                        try
                        {
                            textBox.Line.Visible = Office.MsoTriState.msoTrue;
                            textBox.Line.ForeColor.RGB = 0; // Black
                            textBox.Line.Weight = 0.75f;
                        }
                        catch { }

                        // Set text frame margins
                        try
                        {
                            textBox.TextFrame.MarginLeft = 5;
                            textBox.TextFrame.MarginRight = 5;
                            textBox.TextFrame.MarginTop = 3;
                            textBox.TextFrame.MarginBottom = 3;
                        }
                        catch { }

                        // Set vertical alignment
                        try
                        {
                            textBox.TextFrame.VerticalAnchor = Office.MsoVerticalAnchor.msoAnchorMiddle;
                        }
                        catch { }
                    }
                }

                // Delete the original table
                shape.Delete();

                MessageBox.Show($"Table converted to {rowCount * colCount} text boxes.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error converting table: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
