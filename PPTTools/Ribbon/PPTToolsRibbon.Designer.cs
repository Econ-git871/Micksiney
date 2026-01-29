namespace PPTTools.Ribbon
{
    partial class PPTToolsRibbon : Microsoft.Office.Tools.Ribbon.RibbonBase
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        public PPTToolsRibbon()
            : base(Globals.Factory.GetRibbonFactory())
        {
            InitializeComponent();
        }

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        private void InitializeComponent()
        {
            this.tabPPTTools = this.Factory.CreateRibbonTab();

            // Alignment Group
            this.grpAlignment = this.Factory.CreateRibbonGroup();
            this.btnAlignLeft = this.Factory.CreateRibbonButton();
            this.btnAlignCenter = this.Factory.CreateRibbonButton();
            this.btnAlignRight = this.Factory.CreateRibbonButton();
            this.btnAlignTop = this.Factory.CreateRibbonButton();
            this.btnAlignMiddle = this.Factory.CreateRibbonButton();
            this.btnAlignBottom = this.Factory.CreateRibbonButton();
            this.separator1 = this.Factory.CreateRibbonSeparator();
            this.btnCenterBoth = this.Factory.CreateRibbonButton();
            this.btnDistributeH = this.Factory.CreateRibbonButton();
            this.btnDistributeV = this.Factory.CreateRibbonButton();
            this.btnArrangeGrid = this.Factory.CreateRibbonButton();

            // Formatting Group
            this.grpFormatting = this.Factory.CreateRibbonGroup();
            this.btnMatchWidth = this.Factory.CreateRibbonButton();
            this.btnMatchHeight = this.Factory.CreateRibbonButton();
            this.btnMatchBoth = this.Factory.CreateRibbonButton();
            this.separator2 = this.Factory.CreateRibbonSeparator();
            this.btnCopyFormat = this.Factory.CreateRibbonButton();
            this.btnPasteFormat = this.Factory.CreateRibbonButton();

            // Text Tools Group
            this.grpTextTools = this.Factory.CreateRibbonGroup();
            this.btnMergeTextBoxes = this.Factory.CreateRibbonButton();
            this.btnSplitBySentence = this.Factory.CreateRibbonButton();
            this.btnSplitByParagraph = this.Factory.CreateRibbonButton();

            // Table Tools Group
            this.grpTableTools = this.Factory.CreateRibbonGroup();
            this.btnTableToShapes = this.Factory.CreateRibbonButton();

            // Slide Library Group
            this.grpSlideLibrary = this.Factory.CreateRibbonGroup();
            this.btnSelectLibrary = this.Factory.CreateRibbonButton();
            this.btnInsertFromLibrary = this.Factory.CreateRibbonButton();

            // Slide Utils Group
            this.grpSlideUtils = this.Factory.CreateRibbonGroup();
            this.btnDuplicateWithComments = this.Factory.CreateRibbonButton();

            this.tabPPTTools.SuspendLayout();
            this.grpAlignment.SuspendLayout();
            this.grpFormatting.SuspendLayout();
            this.grpTextTools.SuspendLayout();
            this.grpTableTools.SuspendLayout();
            this.grpSlideLibrary.SuspendLayout();
            this.grpSlideUtils.SuspendLayout();
            this.SuspendLayout();

            //
            // tabPPTTools
            //
            this.tabPPTTools.Groups.Add(this.grpAlignment);
            this.tabPPTTools.Groups.Add(this.grpFormatting);
            this.tabPPTTools.Groups.Add(this.grpTextTools);
            this.tabPPTTools.Groups.Add(this.grpTableTools);
            this.tabPPTTools.Groups.Add(this.grpSlideLibrary);
            this.tabPPTTools.Groups.Add(this.grpSlideUtils);
            this.tabPPTTools.Label = "PPT Tools";
            this.tabPPTTools.Name = "tabPPTTools";

            //
            // grpAlignment
            //
            this.grpAlignment.Items.Add(this.btnAlignLeft);
            this.grpAlignment.Items.Add(this.btnAlignCenter);
            this.grpAlignment.Items.Add(this.btnAlignRight);
            this.grpAlignment.Items.Add(this.btnAlignTop);
            this.grpAlignment.Items.Add(this.btnAlignMiddle);
            this.grpAlignment.Items.Add(this.btnAlignBottom);
            this.grpAlignment.Items.Add(this.separator1);
            this.grpAlignment.Items.Add(this.btnCenterBoth);
            this.grpAlignment.Items.Add(this.btnDistributeH);
            this.grpAlignment.Items.Add(this.btnDistributeV);
            this.grpAlignment.Items.Add(this.btnArrangeGrid);
            this.grpAlignment.Label = "Alignment";
            this.grpAlignment.Name = "grpAlignment";

            // Alignment Buttons
            this.btnAlignLeft.Label = "Left";
            this.btnAlignLeft.Name = "btnAlignLeft";
            this.btnAlignLeft.ScreenTip = "Align Left";
            this.btnAlignLeft.SuperTip = "Align selected shapes to the left";
            this.btnAlignLeft.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignLeft_Click);

            this.btnAlignCenter.Label = "Center";
            this.btnAlignCenter.Name = "btnAlignCenter";
            this.btnAlignCenter.ScreenTip = "Align Center";
            this.btnAlignCenter.SuperTip = "Align selected shapes to center horizontally";
            this.btnAlignCenter.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignCenter_Click);

            this.btnAlignRight.Label = "Right";
            this.btnAlignRight.Name = "btnAlignRight";
            this.btnAlignRight.ScreenTip = "Align Right";
            this.btnAlignRight.SuperTip = "Align selected shapes to the right";
            this.btnAlignRight.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignRight_Click);

            this.btnAlignTop.Label = "Top";
            this.btnAlignTop.Name = "btnAlignTop";
            this.btnAlignTop.ScreenTip = "Align Top";
            this.btnAlignTop.SuperTip = "Align selected shapes to the top";
            this.btnAlignTop.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignTop_Click);

            this.btnAlignMiddle.Label = "Middle";
            this.btnAlignMiddle.Name = "btnAlignMiddle";
            this.btnAlignMiddle.ScreenTip = "Align Middle";
            this.btnAlignMiddle.SuperTip = "Align selected shapes to middle vertically";
            this.btnAlignMiddle.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignMiddle_Click);

            this.btnAlignBottom.Label = "Bottom";
            this.btnAlignBottom.Name = "btnAlignBottom";
            this.btnAlignBottom.ScreenTip = "Align Bottom";
            this.btnAlignBottom.SuperTip = "Align selected shapes to the bottom";
            this.btnAlignBottom.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnAlignBottom_Click);

            this.btnCenterBoth.Label = "Center on Slide";
            this.btnCenterBoth.Name = "btnCenterBoth";
            this.btnCenterBoth.ScreenTip = "Center on Slide";
            this.btnCenterBoth.SuperTip = "Center selected shapes both horizontally and vertically on the slide";
            this.btnCenterBoth.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnCenterBoth_Click);

            this.btnDistributeH.Label = "Distribute H";
            this.btnDistributeH.Name = "btnDistributeH";
            this.btnDistributeH.ScreenTip = "Distribute Horizontally";
            this.btnDistributeH.SuperTip = "Distribute selected shapes evenly horizontally";
            this.btnDistributeH.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnDistributeH_Click);

            this.btnDistributeV.Label = "Distribute V";
            this.btnDistributeV.Name = "btnDistributeV";
            this.btnDistributeV.ScreenTip = "Distribute Vertically";
            this.btnDistributeV.SuperTip = "Distribute selected shapes evenly vertically";
            this.btnDistributeV.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnDistributeV_Click);

            this.btnArrangeGrid.Label = "Grid";
            this.btnArrangeGrid.Name = "btnArrangeGrid";
            this.btnArrangeGrid.ScreenTip = "Arrange in Grid";
            this.btnArrangeGrid.SuperTip = "Arrange selected shapes in a grid pattern";
            this.btnArrangeGrid.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnArrangeGrid_Click);

            //
            // grpFormatting
            //
            this.grpFormatting.Items.Add(this.btnMatchWidth);
            this.grpFormatting.Items.Add(this.btnMatchHeight);
            this.grpFormatting.Items.Add(this.btnMatchBoth);
            this.grpFormatting.Items.Add(this.separator2);
            this.grpFormatting.Items.Add(this.btnCopyFormat);
            this.grpFormatting.Items.Add(this.btnPasteFormat);
            this.grpFormatting.Label = "Formatting";
            this.grpFormatting.Name = "grpFormatting";

            this.btnMatchWidth.Label = "Match Width";
            this.btnMatchWidth.Name = "btnMatchWidth";
            this.btnMatchWidth.ScreenTip = "Match Width";
            this.btnMatchWidth.SuperTip = "Match width of selected shapes to the first selected shape";
            this.btnMatchWidth.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnMatchWidth_Click);

            this.btnMatchHeight.Label = "Match Height";
            this.btnMatchHeight.Name = "btnMatchHeight";
            this.btnMatchHeight.ScreenTip = "Match Height";
            this.btnMatchHeight.SuperTip = "Match height of selected shapes to the first selected shape";
            this.btnMatchHeight.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnMatchHeight_Click);

            this.btnMatchBoth.Label = "Match Both";
            this.btnMatchBoth.Name = "btnMatchBoth";
            this.btnMatchBoth.ScreenTip = "Match Size";
            this.btnMatchBoth.SuperTip = "Match both width and height of selected shapes";
            this.btnMatchBoth.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnMatchBoth_Click);

            this.btnCopyFormat.Label = "Copy Format";
            this.btnCopyFormat.Name = "btnCopyFormat";
            this.btnCopyFormat.ScreenTip = "Copy Format";
            this.btnCopyFormat.SuperTip = "Copy formatting from the selected shape";
            this.btnCopyFormat.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnCopyFormat_Click);

            this.btnPasteFormat.Label = "Paste Format";
            this.btnPasteFormat.Name = "btnPasteFormat";
            this.btnPasteFormat.ScreenTip = "Paste Format";
            this.btnPasteFormat.SuperTip = "Paste copied formatting to selected shapes";
            this.btnPasteFormat.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnPasteFormat_Click);

            //
            // grpTextTools
            //
            this.grpTextTools.Items.Add(this.btnMergeTextBoxes);
            this.grpTextTools.Items.Add(this.btnSplitBySentence);
            this.grpTextTools.Items.Add(this.btnSplitByParagraph);
            this.grpTextTools.Label = "Text Tools";
            this.grpTextTools.Name = "grpTextTools";

            this.btnMergeTextBoxes.Label = "Merge Text";
            this.btnMergeTextBoxes.Name = "btnMergeTextBoxes";
            this.btnMergeTextBoxes.ScreenTip = "Merge Text Boxes";
            this.btnMergeTextBoxes.SuperTip = "Merge multiple text boxes into one";
            this.btnMergeTextBoxes.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnMergeTextBoxes_Click);

            this.btnSplitBySentence.Label = "Split by Sentence";
            this.btnSplitBySentence.Name = "btnSplitBySentence";
            this.btnSplitBySentence.ScreenTip = "Split by Sentence";
            this.btnSplitBySentence.SuperTip = "Split text box into separate boxes by sentence";
            this.btnSplitBySentence.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnSplitBySentence_Click);

            this.btnSplitByParagraph.Label = "Split by Paragraph";
            this.btnSplitByParagraph.Name = "btnSplitByParagraph";
            this.btnSplitByParagraph.ScreenTip = "Split by Paragraph";
            this.btnSplitByParagraph.SuperTip = "Split text box into separate boxes by paragraph";
            this.btnSplitByParagraph.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnSplitByParagraph_Click);

            //
            // grpTableTools
            //
            this.grpTableTools.Items.Add(this.btnTableToShapes);
            this.grpTableTools.Label = "Table Tools";
            this.grpTableTools.Name = "grpTableTools";

            this.btnTableToShapes.Label = "Table to Shapes";
            this.btnTableToShapes.Name = "btnTableToShapes";
            this.btnTableToShapes.ScreenTip = "Convert Table to Shapes";
            this.btnTableToShapes.SuperTip = "Convert the selected table into individual editable text boxes";
            this.btnTableToShapes.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnTableToShapes_Click);

            //
            // grpSlideLibrary
            //
            this.grpSlideLibrary.Items.Add(this.btnSelectLibrary);
            this.grpSlideLibrary.Items.Add(this.btnInsertFromLibrary);
            this.grpSlideLibrary.Label = "Slide Library";
            this.grpSlideLibrary.Name = "grpSlideLibrary";

            this.btnSelectLibrary.Label = "Select Library";
            this.btnSelectLibrary.Name = "btnSelectLibrary";
            this.btnSelectLibrary.ScreenTip = "Select Library File";
            this.btnSelectLibrary.SuperTip = "Select a PowerPoint file to use as your slide library";
            this.btnSelectLibrary.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnSelectLibrary_Click);

            this.btnInsertFromLibrary.Label = "Insert Slide";
            this.btnInsertFromLibrary.Name = "btnInsertFromLibrary";
            this.btnInsertFromLibrary.ScreenTip = "Insert from Library";
            this.btnInsertFromLibrary.SuperTip = "Browse and insert slides from your library";
            this.btnInsertFromLibrary.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnInsertFromLibrary_Click);

            //
            // grpSlideUtils
            //
            this.grpSlideUtils.Items.Add(this.btnDuplicateWithComments);
            this.grpSlideUtils.Label = "Slide Utils";
            this.grpSlideUtils.Name = "grpSlideUtils";

            this.btnDuplicateWithComments.Label = "Duplicate with Comments";
            this.btnDuplicateWithComments.Name = "btnDuplicateWithComments";
            this.btnDuplicateWithComments.ScreenTip = "Duplicate Slide with Comments";
            this.btnDuplicateWithComments.SuperTip = "Duplicate the current slide while preserving all comments";
            this.btnDuplicateWithComments.Click += new Microsoft.Office.Tools.Ribbon.RibbonControlEventHandler(this.btnDuplicateWithComments_Click);

            //
            // PPTToolsRibbon
            //
            this.Name = "PPTToolsRibbon";
            this.RibbonType = "Microsoft.PowerPoint.Presentation";
            this.Tabs.Add(this.tabPPTTools);
            this.Load += new Microsoft.Office.Tools.Ribbon.RibbonUIEventHandler(this.PPTToolsRibbon_Load);
            this.tabPPTTools.ResumeLayout(false);
            this.tabPPTTools.PerformLayout();
            this.grpAlignment.ResumeLayout(false);
            this.grpAlignment.PerformLayout();
            this.grpFormatting.ResumeLayout(false);
            this.grpFormatting.PerformLayout();
            this.grpTextTools.ResumeLayout(false);
            this.grpTextTools.PerformLayout();
            this.grpTableTools.ResumeLayout(false);
            this.grpTableTools.PerformLayout();
            this.grpSlideLibrary.ResumeLayout(false);
            this.grpSlideLibrary.PerformLayout();
            this.grpSlideUtils.ResumeLayout(false);
            this.grpSlideUtils.PerformLayout();
            this.ResumeLayout(false);
        }

        #endregion

        internal Microsoft.Office.Tools.Ribbon.RibbonTab tabPPTTools;

        // Alignment Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpAlignment;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignLeft;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignCenter;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignRight;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignTop;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignMiddle;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnAlignBottom;
        internal Microsoft.Office.Tools.Ribbon.RibbonSeparator separator1;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnCenterBoth;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnDistributeH;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnDistributeV;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnArrangeGrid;

        // Formatting Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpFormatting;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnMatchWidth;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnMatchHeight;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnMatchBoth;
        internal Microsoft.Office.Tools.Ribbon.RibbonSeparator separator2;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnCopyFormat;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnPasteFormat;

        // Text Tools Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpTextTools;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnMergeTextBoxes;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnSplitBySentence;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnSplitByParagraph;

        // Table Tools Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpTableTools;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnTableToShapes;

        // Slide Library Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpSlideLibrary;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnSelectLibrary;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnInsertFromLibrary;

        // Slide Utils Group
        internal Microsoft.Office.Tools.Ribbon.RibbonGroup grpSlideUtils;
        internal Microsoft.Office.Tools.Ribbon.RibbonButton btnDuplicateWithComments;
    }
}
