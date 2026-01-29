using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using Office = Microsoft.Office.Core;

namespace PPTTools.Features.SlideLibrary
{
    public static class SlideLibraryHelper
    {
        private static string _libraryFilePath = null;

        /// <summary>
        /// Get or set the library file path
        /// </summary>
        public static string LibraryFilePath
        {
            get => _libraryFilePath;
            set => _libraryFilePath = value;
        }

        /// <summary>
        /// Open file dialog to select a PowerPoint file as slide library
        /// </summary>
        public static void SelectLibraryFile()
        {
            using (var dialog = new OpenFileDialog())
            {
                dialog.Title = "Select Slide Library File";
                dialog.Filter = "PowerPoint Files|*.pptx;*.pptm;*.ppt|All Files|*.*";
                dialog.FilterIndex = 1;

                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    _libraryFilePath = dialog.FileName;
                    MessageBox.Show($"Slide library set to:\n{_libraryFilePath}", "PPT Tools",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        /// <summary>
        /// Show slide library browser dialog
        /// </summary>
        public static void ShowSlideLibraryDialog()
        {
            if (string.IsNullOrEmpty(_libraryFilePath) || !File.Exists(_libraryFilePath))
            {
                MessageBox.Show("Please select a slide library file first.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                SelectLibraryFile();
                if (string.IsNullOrEmpty(_libraryFilePath)) return;
            }

            using (var dialog = new SlideLibraryDialog(_libraryFilePath))
            {
                if (dialog.ShowDialog() == DialogResult.OK && dialog.SelectedSlideIndices.Count > 0)
                {
                    InsertSlidesFromLibrary(dialog.SelectedSlideIndices);
                }
            }
        }

        /// <summary>
        /// Insert selected slides from library into current presentation
        /// </summary>
        private static void InsertSlidesFromLibrary(List<int> slideIndices)
        {
            var presentation = Globals.ThisAddIn.ActivePresentation;
            var activeSlide = Globals.ThisAddIn.ActiveSlide;

            if (presentation == null)
            {
                MessageBox.Show("No active presentation.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                int insertIndex = activeSlide != null ? activeSlide.SlideIndex : presentation.Slides.Count;

                foreach (int slideIndex in slideIndices)
                {
                    presentation.Slides.InsertFromFile(_libraryFilePath, insertIndex, slideIndex, slideIndex);
                    insertIndex++;
                }

                MessageBox.Show($"{slideIndices.Count} slide(s) inserted.", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error inserting slides: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }

    /// <summary>
    /// Dialog for browsing and selecting slides from library
    /// </summary>
    public class SlideLibraryDialog : Form
    {
        private ListView listView;
        private ImageList imageList;
        private Button btnInsert;
        private Button btnCancel;
        private Button btnSelectAll;
        private Label lblInfo;

        public List<int> SelectedSlideIndices { get; private set; } = new List<int>();

        public SlideLibraryDialog(string libraryPath)
        {
            InitializeComponent();
            LoadSlides(libraryPath);
        }

        private void InitializeComponent()
        {
            this.Text = "Slide Library";
            this.Size = new Size(800, 600);
            this.StartPosition = FormStartPosition.CenterParent;
            this.MinimizeBox = false;

            imageList = new ImageList();
            imageList.ImageSize = new Size(160, 120);
            imageList.ColorDepth = ColorDepth.Depth32Bit;

            listView = new ListView
            {
                Dock = DockStyle.Fill,
                View = View.LargeIcon,
                LargeImageList = imageList,
                MultiSelect = true,
                FullRowSelect = true
            };

            var buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 50
            };

            lblInfo = new Label
            {
                Text = "Select slides to insert (Ctrl+Click for multiple)",
                Left = 10,
                Top = 15,
                Width = 300
            };

            btnSelectAll = new Button
            {
                Text = "Select All",
                Left = 450,
                Top = 10,
                Width = 100
            };
            btnSelectAll.Click += (s, e) =>
            {
                foreach (ListViewItem item in listView.Items)
                    item.Selected = true;
                listView.Focus();
            };

            btnInsert = new Button
            {
                Text = "Insert",
                Left = 560,
                Top = 10,
                Width = 100,
                DialogResult = DialogResult.OK
            };
            btnInsert.Click += (s, e) =>
            {
                foreach (ListViewItem item in listView.SelectedItems)
                {
                    SelectedSlideIndices.Add((int)item.Tag);
                }
            };

            btnCancel = new Button
            {
                Text = "Cancel",
                Left = 670,
                Top = 10,
                Width = 100,
                DialogResult = DialogResult.Cancel
            };

            buttonPanel.Controls.AddRange(new Control[] { lblInfo, btnSelectAll, btnInsert, btnCancel });

            this.Controls.Add(listView);
            this.Controls.Add(buttonPanel);
            this.AcceptButton = btnInsert;
            this.CancelButton = btnCancel;
        }

        private void LoadSlides(string libraryPath)
        {
            try
            {
                var app = Globals.ThisAddIn.PowerPointApp;
                var libPres = app.Presentations.Open(
                    libraryPath,
                    Office.MsoTriState.msoTrue,  // ReadOnly
                    Office.MsoTriState.msoTrue,  // Untitled
                    Office.MsoTriState.msoFalse  // WithWindow
                );

                try
                {
                    for (int i = 1; i <= libPres.Slides.Count; i++)
                    {
                        var slide = libPres.Slides[i];

                        // Export slide as image for thumbnail
                        string tempPath = Path.Combine(Path.GetTempPath(), $"slide_{i}.png");
                        slide.Export(tempPath, "PNG", 320, 240);

                        if (File.Exists(tempPath))
                        {
                            using (var img = Image.FromFile(tempPath))
                            {
                                imageList.Images.Add(new Bitmap(img));
                            }
                            File.Delete(tempPath);
                        }

                        var item = new ListViewItem($"Slide {i}")
                        {
                            ImageIndex = i - 1,
                            Tag = i
                        };
                        listView.Items.Add(item);
                    }

                    lblInfo.Text = $"{libPres.Slides.Count} slides found. Select slides to insert.";
                }
                finally
                {
                    libPres.Close();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading library: {ex.Message}", "PPT Tools",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
