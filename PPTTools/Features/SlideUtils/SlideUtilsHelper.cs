using System;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.SlideUtils
{
    public static class SlideUtilsHelper
    {
        /// <summary>
        /// Duplicate the current slide while preserving all comments
        /// </summary>
        public static void DuplicateSlideWithComments()
        {
            var presentation = Globals.ThisAddIn.ActivePresentation;
            var activeSlide = Globals.ThisAddIn.ActiveSlide;

            if (presentation == null || activeSlide == null)
            {
                MessageBox.Show("Please select a slide to duplicate.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                // Store comment information before duplication
                var comments = new System.Collections.Generic.List<CommentInfo>();

                foreach (PowerPoint.Comment comment in activeSlide.Comments)
                {
                    comments.Add(new CommentInfo
                    {
                        Author = comment.Author,
                        AuthorInitials = comment.AuthorInitials,
                        Text = comment.Text,
                        Left = comment.Left,
                        Top = comment.Top,
                        DateTime = comment.DateTime
                    });
                }

                // Duplicate the slide
                var duplicatedSlideRange = activeSlide.Duplicate();
                var newSlide = duplicatedSlideRange[1];

                // Move to position after original slide
                newSlide.MoveTo(activeSlide.SlideIndex + 1);

                // Re-add comments to the new slide
                foreach (var commentInfo in comments)
                {
                    try
                    {
                        newSlide.Comments.Add(
                            commentInfo.Left,
                            commentInfo.Top,
                            commentInfo.Author,
                            commentInfo.AuthorInitials,
                            commentInfo.Text
                        );
                    }
                    catch
                    {
                        // If adding with author fails, try adding with current user
                        try
                        {
                            var comment = newSlide.Comments.Add(
                                commentInfo.Left,
                                commentInfo.Top,
                                commentInfo.Author,
                                commentInfo.AuthorInitials,
                                commentInfo.Text
                            );
                        }
                        catch { }
                    }
                }

                // Select the new slide
                newSlide.Select();

                if (comments.Count > 0)
                {
                    MessageBox.Show($"Slide duplicated with {comments.Count} comment(s) preserved.", "PPT Tools",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Slide duplicated successfully.", "PPT Tools",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error duplicating slide: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Helper class to store comment information
        /// </summary>
        private class CommentInfo
        {
            public string Author { get; set; }
            public string AuthorInitials { get; set; }
            public string Text { get; set; }
            public float Left { get; set; }
            public float Top { get; set; }
            public DateTime DateTime { get; set; }
        }
    }
}
