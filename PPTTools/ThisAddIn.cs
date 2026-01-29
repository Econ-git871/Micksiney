using System;
using Microsoft.Office.Tools.Ribbon;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools
{
    public partial class ThisAddIn
    {
        /// <summary>
        /// Gets the current PowerPoint application instance
        /// </summary>
        public PowerPoint.Application PowerPointApp => Application;

        /// <summary>
        /// Gets the active presentation, or null if none is open
        /// </summary>
        public PowerPoint.Presentation ActivePresentation
        {
            get
            {
                try
                {
                    return Application.ActivePresentation;
                }
                catch
                {
                    return null;
                }
            }
        }

        /// <summary>
        /// Gets the active slide, or null if none is selected
        /// </summary>
        public PowerPoint.Slide ActiveSlide
        {
            get
            {
                try
                {
                    var window = Application.ActiveWindow;
                    if (window.ViewType == PowerPoint.PpViewType.ppViewSlide ||
                        window.ViewType == PowerPoint.PpViewType.ppViewNormal)
                    {
                        return window.View.Slide as PowerPoint.Slide;
                    }
                    return null;
                }
                catch
                {
                    return null;
                }
            }
        }

        /// <summary>
        /// Gets the selected shapes in the active window
        /// </summary>
        public PowerPoint.ShapeRange SelectedShapes
        {
            get
            {
                try
                {
                    var selection = Application.ActiveWindow.Selection;
                    if (selection.Type == PowerPoint.PpSelectionType.ppSelectionShapes)
                    {
                        return selection.ShapeRange;
                    }
                    return null;
                }
                catch
                {
                    return null;
                }
            }
        }

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            // Initialize add-in
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            // Cleanup
        }

        protected override IRibbonExtensibility CreateRibbonExtensibilityObject()
        {
            return Globals.Factory.GetRibbonFactory().CreateRibbonManager(
                new IRibbonExtension[] { new Ribbon.PPTToolsRibbon() });
        }

        #region VSTO generated code

        private void InternalStartup()
        {
            this.Startup += new System.EventHandler(ThisAddIn_Startup);
            this.Shutdown += new System.EventHandler(ThisAddIn_Shutdown);
        }

        #endregion
    }
}
