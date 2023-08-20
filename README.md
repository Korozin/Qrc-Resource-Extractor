# Qrc Resource Extractor

This is a simple program to parse and create images from the data assigned to the `qt_resource_data` variable that is created when you convert a `.qrc` file using `pyrcc`

`.qrc` files are what hold image data in the form of a "resource" for use in Qt Designer. `pyrcc` is what converts those `.qrc` files into Python form.

### Note!
This tool only supports the following formats!

-   PNG
-   JPG / JPEG
-   SVG

Unfortunately if any other file types exist in the resource data, the program will stop there. I'm too lazy to fix that. But since the supported formats are also the most common, it should be more or less fine.

> Example usage can be found in [Example](https://github.com/Korozin/Qrc-Resource-Extractor/tree/main/Example)
