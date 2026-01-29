# PPT Tools - PowerPoint Productivity Add-in

A VSTO-based PowerPoint add-in that provides professional productivity tools for creating presentations faster.

## Features

### Alignment & Layout
- **Smart Align** - Align shapes to left, center, right, top, middle, bottom (relative to first selected)
- **Center on Slide** - Center shapes both horizontally and vertically
- **Distribute** - Evenly distribute shapes horizontally or vertically
- **Grid Arrange** - Arrange shapes in a customizable grid pattern

### Formatting
- **Match Size** - Match width, height, or both to the first selected shape
- **Enhanced Format Painter** - Copy and paste shape formatting (fill, line, shadow)

### Text Tools
- **Merge Text Boxes** - Combine multiple text boxes into one
- **Split by Sentence** - Split text box into separate boxes by sentence
- **Split by Paragraph** - Split text box into separate boxes by paragraph

### Table Tools
- **Table to Shapes** - Convert tables into individual editable text boxes

### Slide Library
- **Custom Library** - Select a PowerPoint file as your slide library
- **Quick Insert** - Browse and insert slides from your library

### Slide Utils
- **Duplicate with Comments** - Duplicate slides while preserving all comments

## Requirements

- Windows 10/11
- Microsoft PowerPoint 2016 or later (Office 365 recommended)
- Visual Studio 2019/2022 with "Office/SharePoint development" workload
- .NET Framework 4.8

## Installation

### For Development

1. Install Visual Studio 2022 with "Office/SharePoint development" workload
2. Clone or download this repository
3. Open `PPTTools.sln` in Visual Studio
4. Press F5 to build and debug

### For Deployment

1. Build the solution in Release mode
2. Run the installer or deploy via ClickOnce

## Project Structure

```
PPTTools/
├── PPTTools.sln              # Solution file
├── PPTTools.csproj           # Project file
├── ThisAddIn.cs              # Main add-in entry point
├── app.config                # Application configuration
├── Properties/
│   └── AssemblyInfo.cs       # Assembly information
├── Ribbon/
│   ├── PPTToolsRibbon.cs     # Ribbon event handlers
│   ├── PPTToolsRibbon.Designer.cs  # Ribbon UI definition
│   └── PPTToolsRibbon.resx   # Ribbon resources
├── Features/
│   ├── Alignment/
│   │   └── AlignmentHelper.cs
│   ├── Formatting/
│   │   └── FormattingHelper.cs
│   ├── TextTools/
│   │   └── TextToolsHelper.cs
│   ├── TableTools/
│   │   └── TableToShapesHelper.cs
│   ├── SlideLibrary/
│   │   └── SlideLibraryHelper.cs
│   └── SlideUtils/
│       └── SlideUtilsHelper.cs
└── Helpers/
    └── ShapeHelper.cs        # Utility methods
```

## Usage

After installation, a new "PPT Tools" tab will appear in the PowerPoint ribbon.

### Alignment
1. Select 2 or more shapes
2. Click alignment buttons (Left, Center, Right, Top, Middle, Bottom)
3. Shapes align relative to the first selected shape

### Grid Arrange
1. Select shapes to arrange
2. Click "Grid" button
3. Set rows, columns, and spacing
4. Click OK

### Table to Shapes
1. Select a table
2. Click "Table to Shapes"
3. Table converts to individual text boxes

### Slide Library
1. Click "Select Library" to choose a PowerPoint file
2. Click "Insert Slide" to browse and insert slides

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
