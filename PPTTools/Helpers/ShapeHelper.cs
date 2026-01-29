using System;
using System.Collections.Generic;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Helpers
{
    /// <summary>
    /// Utility methods for working with PowerPoint shapes
    /// </summary>
    public static class ShapeHelper
    {
        /// <summary>
        /// Convert ShapeRange to a List of shapes
        /// </summary>
        public static List<PowerPoint.Shape> ToList(PowerPoint.ShapeRange shapeRange)
        {
            var list = new List<PowerPoint.Shape>();
            if (shapeRange != null)
            {
                for (int i = 1; i <= shapeRange.Count; i++)
                {
                    list.Add(shapeRange[i]);
                }
            }
            return list;
        }

        /// <summary>
        /// Get the bounding box of a collection of shapes
        /// </summary>
        public static (float Left, float Top, float Width, float Height) GetBoundingBox(IEnumerable<PowerPoint.Shape> shapes)
        {
            float minLeft = float.MaxValue, minTop = float.MaxValue;
            float maxRight = float.MinValue, maxBottom = float.MinValue;

            foreach (var shape in shapes)
            {
                minLeft = Math.Min(minLeft, shape.Left);
                minTop = Math.Min(minTop, shape.Top);
                maxRight = Math.Max(maxRight, shape.Left + shape.Width);
                maxBottom = Math.Max(maxBottom, shape.Top + shape.Height);
            }

            return (minLeft, minTop, maxRight - minLeft, maxBottom - minTop);
        }

        /// <summary>
        /// Check if shape is a text box or has text frame
        /// </summary>
        public static bool IsTextShape(PowerPoint.Shape shape)
        {
            return shape.HasTextFrame == Office.MsoTriState.msoTrue;
        }

        /// <summary>
        /// Check if shape is a table
        /// </summary>
        public static bool IsTable(PowerPoint.Shape shape)
        {
            return shape.HasTable;
        }

        /// <summary>
        /// Get the center point of a shape
        /// </summary>
        public static (float X, float Y) GetCenter(PowerPoint.Shape shape)
        {
            return (shape.Left + shape.Width / 2, shape.Top + shape.Height / 2);
        }

        /// <summary>
        /// Set the center point of a shape (moves the shape)
        /// </summary>
        public static void SetCenter(PowerPoint.Shape shape, float centerX, float centerY)
        {
            shape.Left = centerX - shape.Width / 2;
            shape.Top = centerY - shape.Height / 2;
        }

        /// <summary>
        /// Copy shape formatting from source to target
        /// </summary>
        public static void CopyFormatting(PowerPoint.Shape source, PowerPoint.Shape target)
        {
            try
            {
                source.PickUp();
                target.Apply();
            }
            catch
            {
                // Manual copy if PickUp/Apply fails
                CopyFormattingManual(source, target);
            }
        }

        /// <summary>
        /// Manual formatting copy when PickUp/Apply fails
        /// </summary>
        private static void CopyFormattingManual(PowerPoint.Shape source, PowerPoint.Shape target)
        {
            try
            {
                // Copy fill
                if (source.Fill.Type == Office.MsoFillType.msoFillSolid)
                {
                    target.Fill.Solid();
                    target.Fill.ForeColor.RGB = source.Fill.ForeColor.RGB;
                    target.Fill.Transparency = source.Fill.Transparency;
                }

                // Copy line
                target.Line.Visible = source.Line.Visible;
                if (source.Line.Visible == Office.MsoTriState.msoTrue)
                {
                    target.Line.ForeColor.RGB = source.Line.ForeColor.RGB;
                    target.Line.Weight = source.Line.Weight;
                    target.Line.DashStyle = source.Line.DashStyle;
                }

                // Copy shadow
                target.Shadow.Visible = source.Shadow.Visible;
            }
            catch { }
        }
    }
}
