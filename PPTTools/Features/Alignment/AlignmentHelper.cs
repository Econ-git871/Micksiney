using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.Alignment
{
    public enum AlignmentType
    {
        Left,
        Center,
        Right,
        Top,
        Middle,
        Bottom
    }

    public static class AlignmentHelper
    {
        /// <summary>
        /// Align selected shapes based on alignment type
        /// </summary>
        public static void AlignShapes(AlignmentType alignType)
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count < 2)
            {
                MessageBox.Show("Please select at least 2 shapes to align.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                // Get the first shape as reference
                var referenceShape = shapes[1];
                float referenceValue = 0;

                switch (alignType)
                {
                    case AlignmentType.Left:
                        referenceValue = referenceShape.Left;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Left = referenceValue;
                        break;

                    case AlignmentType.Center:
                        referenceValue = referenceShape.Left + referenceShape.Width / 2;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Left = referenceValue - shapes[i].Width / 2;
                        break;

                    case AlignmentType.Right:
                        referenceValue = referenceShape.Left + referenceShape.Width;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Left = referenceValue - shapes[i].Width;
                        break;

                    case AlignmentType.Top:
                        referenceValue = referenceShape.Top;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Top = referenceValue;
                        break;

                    case AlignmentType.Middle:
                        referenceValue = referenceShape.Top + referenceShape.Height / 2;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Top = referenceValue - shapes[i].Height / 2;
                        break;

                    case AlignmentType.Bottom:
                        referenceValue = referenceShape.Top + referenceShape.Height;
                        for (int i = 2; i <= shapes.Count; i++)
                            shapes[i].Top = referenceValue - shapes[i].Height;
                        break;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error aligning shapes: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Center selected shapes on the slide (both horizontally and vertically)
        /// </summary>
        public static void CenterOnSlide()
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            var slide = Globals.ThisAddIn.ActiveSlide;

            if (shapes == null || shapes.Count == 0 || slide == null)
            {
                MessageBox.Show("Please select at least one shape.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var presentation = Globals.ThisAddIn.ActivePresentation;
                float slideWidth = presentation.PageSetup.SlideWidth;
                float slideHeight = presentation.PageSetup.SlideHeight;

                if (shapes.Count == 1)
                {
                    // Center single shape on slide
                    var shape = shapes[1];
                    shape.Left = (slideWidth - shape.Width) / 2;
                    shape.Top = (slideHeight - shape.Height) / 2;
                }
                else
                {
                    // Calculate bounding box of all shapes
                    float minLeft = float.MaxValue, minTop = float.MaxValue;
                    float maxRight = float.MinValue, maxBottom = float.MinValue;

                    for (int i = 1; i <= shapes.Count; i++)
                    {
                        var shape = shapes[i];
                        minLeft = Math.Min(minLeft, shape.Left);
                        minTop = Math.Min(minTop, shape.Top);
                        maxRight = Math.Max(maxRight, shape.Left + shape.Width);
                        maxBottom = Math.Max(maxBottom, shape.Top + shape.Height);
                    }

                    float groupWidth = maxRight - minLeft;
                    float groupHeight = maxBottom - minTop;
                    float offsetX = (slideWidth - groupWidth) / 2 - minLeft;
                    float offsetY = (slideHeight - groupHeight) / 2 - minTop;

                    // Move all shapes
                    for (int i = 1; i <= shapes.Count; i++)
                    {
                        shapes[i].Left += offsetX;
                        shapes[i].Top += offsetY;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error centering shapes: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Distribute shapes evenly
        /// </summary>
        public static void DistributeShapes(bool horizontal)
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count < 3)
            {
                MessageBox.Show("Please select at least 3 shapes to distribute.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var shapeList = new List<PowerPoint.Shape>();
                for (int i = 1; i <= shapes.Count; i++)
                    shapeList.Add(shapes[i]);

                if (horizontal)
                {
                    // Sort by left position
                    shapeList = shapeList.OrderBy(s => s.Left).ToList();

                    float totalWidth = shapeList.Sum(s => s.Width);
                    float startX = shapeList.First().Left;
                    float endX = shapeList.Last().Left + shapeList.Last().Width;
                    float availableSpace = endX - startX - totalWidth;
                    float gap = availableSpace / (shapeList.Count - 1);

                    float currentX = startX;
                    foreach (var shape in shapeList)
                    {
                        shape.Left = currentX;
                        currentX += shape.Width + gap;
                    }
                }
                else
                {
                    // Sort by top position
                    shapeList = shapeList.OrderBy(s => s.Top).ToList();

                    float totalHeight = shapeList.Sum(s => s.Height);
                    float startY = shapeList.First().Top;
                    float endY = shapeList.Last().Top + shapeList.Last().Height;
                    float availableSpace = endY - startY - totalHeight;
                    float gap = availableSpace / (shapeList.Count - 1);

                    float currentY = startY;
                    foreach (var shape in shapeList)
                    {
                        shape.Top = currentY;
                        currentY += shape.Height + gap;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error distributing shapes: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Show grid arrangement dialog
        /// </summary>
        public static void ShowGridArrangeDialog()
        {
            var shapes = Globals.ThisAddIn.SelectedShapes;
            if (shapes == null || shapes.Count < 2)
            {
                MessageBox.Show("Please select at least 2 shapes to arrange in a grid.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            using (var dialog = new GridArrangeDialog(shapes.Count))
            {
                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    ArrangeInGrid(shapes, dialog.Rows, dialog.Columns, dialog.HorizontalSpacing, dialog.VerticalSpacing);
                }
            }
        }

        /// <summary>
        /// Arrange shapes in a grid pattern
        /// </summary>
        private static void ArrangeInGrid(PowerPoint.ShapeRange shapes, int rows, int columns, float hSpacing, float vSpacing)
        {
            try
            {
                var shapeList = new List<PowerPoint.Shape>();
                for (int i = 1; i <= shapes.Count; i++)
                    shapeList.Add(shapes[i]);

                // Use first shape's position as starting point
                float startX = shapeList[0].Left;
                float startY = shapeList[0].Top;

                // Get max dimensions for uniform spacing
                float maxWidth = shapeList.Max(s => s.Width);
                float maxHeight = shapeList.Max(s => s.Height);

                int index = 0;
                for (int row = 0; row < rows && index < shapeList.Count; row++)
                {
                    for (int col = 0; col < columns && index < shapeList.Count; col++)
                    {
                        var shape = shapeList[index];
                        shape.Left = startX + col * (maxWidth + hSpacing);
                        shape.Top = startY + row * (maxHeight + vSpacing);
                        index++;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error arranging shapes in grid: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }

    /// <summary>
    /// Dialog for grid arrangement settings
    /// </summary>
    public class GridArrangeDialog : Form
    {
        private NumericUpDown numRows;
        private NumericUpDown numColumns;
        private NumericUpDown numHSpacing;
        private NumericUpDown numVSpacing;
        private Button btnOK;
        private Button btnCancel;

        public int Rows => (int)numRows.Value;
        public int Columns => (int)numColumns.Value;
        public float HorizontalSpacing => (float)numHSpacing.Value;
        public float VerticalSpacing => (float)numVSpacing.Value;

        public GridArrangeDialog(int shapeCount)
        {
            InitializeComponent(shapeCount);
        }

        private void InitializeComponent(int shapeCount)
        {
            this.Text = "Arrange in Grid";
            this.Size = new System.Drawing.Size(300, 220);
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.StartPosition = FormStartPosition.CenterParent;
            this.MaximizeBox = false;
            this.MinimizeBox = false;

            int defaultCols = (int)Math.Ceiling(Math.Sqrt(shapeCount));
            int defaultRows = (int)Math.Ceiling((double)shapeCount / defaultCols);

            var lblRows = new Label { Text = "Rows:", Left = 20, Top = 20, Width = 80 };
            numRows = new NumericUpDown { Left = 110, Top = 18, Width = 80, Minimum = 1, Maximum = 100, Value = defaultRows };

            var lblColumns = new Label { Text = "Columns:", Left = 20, Top = 50, Width = 80 };
            numColumns = new NumericUpDown { Left = 110, Top = 48, Width = 80, Minimum = 1, Maximum = 100, Value = defaultCols };

            var lblHSpacing = new Label { Text = "H Spacing (pt):", Left = 20, Top = 80, Width = 80 };
            numHSpacing = new NumericUpDown { Left = 110, Top = 78, Width = 80, Minimum = 0, Maximum = 500, Value = 10 };

            var lblVSpacing = new Label { Text = "V Spacing (pt):", Left = 20, Top = 110, Width = 80 };
            numVSpacing = new NumericUpDown { Left = 110, Top = 108, Width = 80, Minimum = 0, Maximum = 500, Value = 10 };

            btnOK = new Button { Text = "OK", Left = 50, Top = 145, Width = 80, DialogResult = DialogResult.OK };
            btnCancel = new Button { Text = "Cancel", Left = 150, Top = 145, Width = 80, DialogResult = DialogResult.Cancel };

            this.Controls.AddRange(new Control[] { lblRows, numRows, lblColumns, numColumns, lblHSpacing, numHSpacing, lblVSpacing, numVSpacing, btnOK, btnCancel });
            this.AcceptButton = btnOK;
            this.CancelButton = btnCancel;
        }
    }
}
