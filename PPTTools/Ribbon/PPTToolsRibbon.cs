using System;
using System.Windows.Forms;
using Microsoft.Office.Tools.Ribbon;
using PPTTools.Features.Alignment;
using PPTTools.Features.Formatting;
using PPTTools.Features.TextTools;
using PPTTools.Features.TableTools;
using PPTTools.Features.SlideLibrary;
using PPTTools.Features.SlideUtils;

namespace PPTTools.Ribbon
{
    public partial class PPTToolsRibbon
    {
        private void PPTToolsRibbon_Load(object sender, RibbonUIEventArgs e)
        {
        }

        #region Alignment Buttons

        private void btnAlignLeft_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Left);
        }

        private void btnAlignCenter_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Center);
        }

        private void btnAlignRight_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Right);
        }

        private void btnAlignTop_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Top);
        }

        private void btnAlignMiddle_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Middle);
        }

        private void btnAlignBottom_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.AlignShapes(AlignmentType.Bottom);
        }

        private void btnCenterBoth_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.CenterOnSlide();
        }

        private void btnArrangeGrid_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.ShowGridArrangeDialog();
        }

        private void btnDistributeH_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.DistributeShapes(true);
        }

        private void btnDistributeV_Click(object sender, RibbonControlEventArgs e)
        {
            AlignmentHelper.DistributeShapes(false);
        }

        #endregion

        #region Formatting Buttons

        private void btnMatchWidth_Click(object sender, RibbonControlEventArgs e)
        {
            FormattingHelper.MatchSize(SizeMatchType.Width);
        }

        private void btnMatchHeight_Click(object sender, RibbonControlEventArgs e)
        {
            FormattingHelper.MatchSize(SizeMatchType.Height);
        }

        private void btnMatchBoth_Click(object sender, RibbonControlEventArgs e)
        {
            FormattingHelper.MatchSize(SizeMatchType.Both);
        }

        private void btnCopyFormat_Click(object sender, RibbonControlEventArgs e)
        {
            FormattingHelper.CopyFormat();
        }

        private void btnPasteFormat_Click(object sender, RibbonControlEventArgs e)
        {
            FormattingHelper.PasteFormat();
        }

        #endregion

        #region Text Tools Buttons

        private void btnMergeTextBoxes_Click(object sender, RibbonControlEventArgs e)
        {
            TextToolsHelper.MergeTextBoxes();
        }

        private void btnSplitBySentence_Click(object sender, RibbonControlEventArgs e)
        {
            TextToolsHelper.SplitTextBox(SplitMode.BySentence);
        }

        private void btnSplitByParagraph_Click(object sender, RibbonControlEventArgs e)
        {
            TextToolsHelper.SplitTextBox(SplitMode.ByParagraph);
        }

        #endregion

        #region Table Tools Buttons

        private void btnTableToShapes_Click(object sender, RibbonControlEventArgs e)
        {
            TableToShapesHelper.ConvertTableToShapes();
        }

        #endregion

        #region Slide Library Buttons

        private void btnSelectLibrary_Click(object sender, RibbonControlEventArgs e)
        {
            SlideLibraryHelper.SelectLibraryFile();
        }

        private void btnInsertFromLibrary_Click(object sender, RibbonControlEventArgs e)
        {
            SlideLibraryHelper.ShowSlideLibraryDialog();
        }

        #endregion

        #region Slide Utils Buttons

        private void btnDuplicateWithComments_Click(object sender, RibbonControlEventArgs e)
        {
            SlideUtilsHelper.DuplicateSlideWithComments();
        }

        #endregion
    }
}
