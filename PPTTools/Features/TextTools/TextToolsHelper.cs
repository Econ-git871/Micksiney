using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.TextTools
{
    public enum SplitMode
    {
        BySentence,
        ByParagraph
    }

    public static class TextToolsHelper
    {
        /// <summary>
        /// Merge multiple text boxes into one
        /// </summary>
        public static void MergeTextBoxes()
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            var slide = Globals.ThisAddIn.ActiveSlide;

            if (shapes == null || shapes.Count < 2 || slide == null)
            {
                MessageBox.Show("Please select at least 2 text boxes to merge.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                // Collect text boxes and sort by position (top to bottom, left to right)
                var textShapes = new List<PowerPoint.Shape>();
                for (int i = 1; i <= shapes.Count; i++)
                {
                    var shape = shapes[i];
                    if (shape.HasTextFrame == Office.MsoTriState.msoTrue)
                    {
                        textShapes.Add(shape);
                    }
                }

                if (textShapes.Count < 2)
                {
                    MessageBox.Show("Please select at least 2 shapes with text.", "PPT Tools",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                // Sort by position (top to bottom, then left to right)
                textShapes.Sort((a, b) =>
                {
                    int topCompare = a.Top.CompareTo(b.Top);
                    return topCompare != 0 ? topCompare : a.Left.CompareTo(b.Left);
                });

                // Calculate bounding box
                float minLeft = float.MaxValue, minTop = float.MaxValue;
                float maxRight = float.MinValue, maxBottom = float.MinValue;

                foreach (var shape in textShapes)
                {
                    minLeft = Math.Min(minLeft, shape.Left);
                    minTop = Math.Min(minTop, shape.Top);
                    maxRight = Math.Max(maxRight, shape.Left + shape.Width);
                    maxBottom = Math.Max(maxBottom, shape.Top + shape.Height);
                }

                // Collect all text
                var allText = new List<string>();
                foreach (var shape in textShapes)
                {
                    string text = shape.TextFrame.TextRange.Text.Trim();
                    if (!string.IsNullOrEmpty(text))
                    {
                        allText.Add(text);
                    }
                }

                // Create new text box
                var newShape = slide.Shapes.AddTextbox(
                    Office.MsoTextOrientation.msoTextOrientationHorizontal,
                    minLeft, minTop, maxRight - minLeft, maxBottom - minTop);

                // Set merged text
                newShape.TextFrame.TextRange.Text = string.Join("\n", allText);

                // Copy formatting from first text box
                var firstShape = textShapes[0];
                try
                {
                    var srcFont = firstShape.TextFrame.TextRange.Font;
                    var dstFont = newShape.TextFrame.TextRange.Font;
                    dstFont.Name = srcFont.Name;
                    dstFont.Size = srcFont.Size;
                    dstFont.Color.RGB = srcFont.Color.RGB;
                    dstFont.Bold = srcFont.Bold;
                    dstFont.Italic = srcFont.Italic;
                }
                catch { }

                // Delete original shapes
                foreach (var shape in textShapes)
                {
                    shape.Delete();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error merging text boxes: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Split text box by sentence or paragraph
        /// </summary>
        public static void SplitTextBox(SplitMode mode)
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            var slide = Globals.ThisAddIn.ActiveSlide;

            if (shapes == null || shapes.Count != 1 || slide == null)
            {
                MessageBox.Show("Please select exactly one text box to split.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            var shape = shapes[1];
            if (shape.HasTextFrame != Office.MsoTriState.msoTrue ||
                string.IsNullOrWhiteSpace(shape.TextFrame.TextRange.Text))
            {
                MessageBox.Show("Selected shape must contain text.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                string text = shape.TextFrame.TextRange.Text;
                string[] parts;

                if (mode == SplitMode.BySentence)
                {
                    // Split by sentence (. ! ?)
                    parts = Regex.Split(text, @"(?<=[.!?])\s+");
                }
                else
                {
                    // Split by paragraph (newlines)
                    parts = text.Split(new[] { "\r\n", "\r", "\n" }, StringSplitOptions.RemoveEmptyEntries);
                }

                if (parts.Length < 2)
                {
                    MessageBox.Show("Text cannot be split further.", "PPT Tools",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                // Store original shape properties
                float left = shape.Left;
                float top = shape.Top;
                float width = shape.Width;
                float height = shape.Height / parts.Length;

                // Store font properties
                string fontName = "Calibri";
                float fontSize = 11;
                int fontColor = 0;
                Office.MsoTriState fontBold = Office.MsoTriState.msoFalse;
                Office.MsoTriState fontItalic = Office.MsoTriState.msoFalse;

                try
                {
                    var srcFont = shape.TextFrame.TextRange.Font;
                    fontName = srcFont.Name;
                    fontSize = srcFont.Size;
                    fontColor = srcFont.Color.RGB;
                    fontBold = srcFont.Bold;
                    fontItalic = srcFont.Italic;
                }
                catch { }

                // Create new text boxes for each part
                float currentTop = top;
                float spacing = 5; // Gap between boxes

                foreach (string part in parts)
                {
                    string trimmedPart = part.Trim();
                    if (string.IsNullOrEmpty(trimmedPart)) continue;

                    var newShape = slide.Shapes.AddTextbox(
                        Office.MsoTextOrientation.msoTextOrientationHorizontal,
                        left, currentTop, width, height);

                    newShape.TextFrame.TextRange.Text = trimmedPart;
                    newShape.TextFrame.AutoSize = PowerPoint.PpAutoSize.ppAutoSizeShapeToFitText;

                    // Apply formatting
                    try
                    {
                        var dstFont = newShape.TextFrame.TextRange.Font;
                        dstFont.Name = fontName;
                        dstFont.Size = fontSize;
                        dstFont.Color.RGB = fontColor;
                        dstFont.Bold = fontBold;
                        dstFont.Italic = fontItalic;
                    }
                    catch { }

                    currentTop += newShape.Height + spacing;
                }

                // Delete original shape
                shape.Delete();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error splitting text box: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
