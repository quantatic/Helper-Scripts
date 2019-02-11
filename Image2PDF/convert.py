import fpdf
import PIL

import argparse
import os

def make_pdf(list_images, output_file):

    if not list_images:
        raise Exception("List of image filenames cannot be empty")

    dimensions = [PIL.Image.open(image).size for image in list_images]
    max_dimension = [max(dimensions, key=lambda x:x[n])[n] for n in range(len(dimensions[0]))] #find the overall maximum dimensions

    pdf = fpdf.FPDF(unit="pt", format=max_dimension)

    for page_image in list_images:
        pdf.add_page()
        pdf.image(page_image, 0, 0)

    pdf.output(output_file, "F")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts an arbitrary number of input images from a given directory to a PDF.")
    parser.add_argument("directory", help="the directory containing the images to be converted")
    parser.add_argument("extension", help="the file extension of the images to convert", choices=['png', 'jpg', 'jpeg'])
    parser.add_argument("output", help="the path of the output file")
    parser.add_argument("-v", "--verbose", help="increases verbosity of program output", action="store_true")
    args = parser.parse_args()

    images = ["{}/{}".format(args.directory, image) for image in os.listdir(args.directory) if image.endswith(args.extension)]
    if not images:
        raise Exception("[+] {}/*.{} returned no results".format(args.directory, args.extension))

    if not args.output.endswith(".pdf"):
        print("[+] Warning: {} does not appear to be a valid PDF filename. Continuing anyways...".format(args.output))

    if args.verbose:
        print("[+] Writing {} to {}".format(", ".join(images), args.output))
        
    make_pdf(images, args.output)

    if args.verbose:
        print("[+] {} have successfully been written to {}".format(", ".join(images), args.output))
