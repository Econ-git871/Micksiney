using System;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.Formatting
{
    public enum SizeMatchType
    {
        Width,
        Height,
        Both
    }

    /// <summary>
    /// Stored format information for copy/paste operations
    /// </summary>
    public class StoredFormat
    {
        public float Width { get; set; }
        public float Height { get; set; }
        public float Left { get; set; }
        public float Top { get; set; }

        // Fill properties
        public Office.MsoFillType FillType { get; set; }
        public int FillForeColor { get; set; }
        public int FillBackColor { get; set; }
        public float FillTransparency { get; set; }

        // Line properties
        public Office.MsoLineStyle LineStyle { get; set; }
        public float LineWeight { get; set; }
        public int LineColor { get; set; }
        public Office.MsoLineDashStyle LineDashStyle { get; set; }
        public float LineTransparency { get; set; }
        public bool LineVisible { get; set; }

        // Shadow properties
        public bool ShadowVisible { get; set; }
        public Office.MsoShadowType ShadowType { get; set; }
        public int ShadowColor { get; set; }
        public float ShadowBlur { get; set; }
        public float ShadowOffsetX { get; set; }
        public float ShadowOffsetY { get; set; }
        public float ShadowTransparency { get; set; }
    }

    public static class FormattingHelper
    {
        private static StoredFormat _copiedFormat = null;

        /// <summary>
        /// Match size of selected shapes to the first selected shape
        /// </summary>
        public static void MatchSize(SizeMatchType matchType)
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count < 2)
            {
                MessageBox.Show("Please select at least 2 shapes.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var referenceShape = shapes[1];
                float targetWidth = referenceShape.Width;
                float targetHeight = referenceShape.Height;

                for (int i = 2; i <= shapes.Count; i++)
                {
                    var shape = shapes[i];

                    // Calculate center point to maintain position
                    float centerX = shape.Left + shape.Width / 2;
                    float centerY = shape.Top + shape.Height / 2;

                    switch (matchType)
                    {
                        case SizeMatchType.Width:
                            shape.Width = targetWidth;
                            shape.Left = centerX - shape.Width / 2;
                            break;

                        case SizeMatchType.Height:
                            shape.Height = targetHeight;
                            shape.Top = centerY - shape.Height / 2;
                            break;

                        case SizeMatchType.Both:
                            shape.Width = targetWidth;
                            shape.Height = targetHeight;
                            shape.Left = centerX - shape.Width / 2;
                            shape.Top = centerY - shape.Height / 2;
                            break;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error matching size: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Copy format from the selected shape
        /// </summary>
        public static void CopyFormat()
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count != 1)
            {
                MessageBox.Show("Please select exactly one shape to copy format from.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var shape = shapes[1];
                _copiedFormat = new StoredFormat
                {
                    Width = shape.Width,
                    Height = shape.Height,
                    Left = shape.Left,
                    Top = shape.Top
                };

                // Copy fill properties
                if (shape.Fill != null)
                {
                    _copiedFormat.FillType = shape.Fill.Type;
                    _copiedFormat.FillTransparency = shape.Fill.Transparency;

                    try
                    {
                        _copiedFormat.FillForeColor = shape.Fill.ForeColor.RGB;
                        _copiedFormat.FillBackColor = shape.Fill.BackColor.RGB;
                    }
                    catch { }
                }

                // Copy line properties
                if (shape.Line != null)
                {
                    _copiedFormat.LineVisible = shape.Line.Visible == Office.MsoTriState.msoTrue;
                    if (_copiedFormat.LineVisible)
                    {
                        _copiedFormat.LineStyle = shape.Line.Style;
                        _copiedFormat.LineWeight = shape.Line.Weight;
                        _copiedFormat.LineDashStyle = shape.Line.DashStyle;
                        _copiedFormat.LineTransparency = shape.Line.Transparency;
                        try
                        {
                            _copiedFormat.LineColor = shape.Line.ForeColor.RGB;
                        }
                        catch { }
                    }
                }

                // Copy shadow properties
                if (shape.Shadow != null)
                {
                    _copiedFormat.ShadowVisible = shape.Shadow.Visible == Office.MsoTriState.msoTrue;
                    if (_copiedFormat.ShadowVisible)
                    {
                        _copiedFormat.ShadowType = shape.Shadow.Type;
                        _copiedFormat.ShadowBlur = shape.Shadow.Blur;
                        _copiedFormat.ShadowOffsetX = shape.Shadow.OffsetX;
                        _copiedFormat.ShadowOffsetY = shape.Shadow.OffsetY;
                        _copiedFormat.ShadowTransparency = shape.Shadow.Transparency;
                        try
                        {
                            _copiedFormat.ShadowColor = shape.Shadow.ForeColor.RGB;
                        }
                        catch { }
                    }
                }

                MessageBox.Show("Format copied successfully!", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error copying format: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Paste format to selected shapes
        /// </summary>
        public static void PasteFormat()
        {
            if (_copiedFormat == null)
            {
                MessageBox.Show("No format has been copied. Please copy a format first.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count == 0)
            {
                MessageBox.Show("Please select at least one shape to paste format to.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                for (int i = 1; i <= shapes.Count; i++)
                {
                    var shape = shapes[i];
                    ApplyFormat(shape, _copiedFormat);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error pasting format: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Apply stored format to a shape
        /// </summary>
        private static void ApplyFormat(PowerPoint.Shape shape, StoredFormat format)
        {
            // Apply fill
            if (shape.Fill != null)
            {
                try
                {
                    if (format.FillType == Office.MsoFillType.msoFillSolid)
                    {
                        shape.Fill.Solid();
                        shape.Fill.ForeColor.RGB = format.FillForeColor;
                    }
                    shape.Fill.Transparency = format.FillTransparency;
                }
                catch { }
            }

            // Apply line
            if (shape.Line != null)
            {
                try
                {
                    shape.Line.Visible = format.LineVisible ? Office.MsoTriState.msoTrue : Office.MsoTriState.msoFalse;
                    if (format.LineVisible)
                    {
                        shape.Line.Style = format.LineStyle;
                        shape.Line.Weight = format.LineWeight;
                        shape.Line.DashStyle = format.LineDashStyle;
                        shape.Line.ForeColor.RGB = format.LineColor;
                        shape.Line.Transparency = format.LineTransparency;
                    }
                }
                catch { }
            }

            // Apply shadow
            if (shape.Shadow != null)
            {
                try
                {
                    shape.Shadow.Visible = format.ShadowVisible ? Office.MsoTriState.msoTrue : Office.MsoTriState.msoFalse;
                    if (format.ShadowVisible)
                    {
                        shape.Shadow.Type = format.ShadowType;
                        shape.Shadow.Blur = format.ShadowBlur;
                        shape.Shadow.OffsetX = format.ShadowOffsetX;
                        shape.Shadow.OffsetY = format.ShadowOffsetY;
                        shape.Shadow.ForeColor.RGB = format.ShadowColor;
                        shape.Shadow.Transparency = format.ShadowTransparency;
                    }
                }
                catch { }
            }
        }
    }
}
