import os
from pathlib import Path

def _create_html_page(svg_files, output_path="steps/index.html"):
    # HTML head content
    head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Steps</title>
        <style>
html {
    background: black;
}
.steps {
    width: 100%;
    height: 100vh; /* Takes full viewport height */
    position: relative;
}

.steps > object {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0; /* Initially hide all SVGs */
    transition: opacity 0.05s ease; /* Transition effect */
}
    </style>
    </head>
    <body>
    """

    # HTML navigation buttons
    #  <button onclick="previousSVG()">Previous</button>
    #  <button onclick="nextSVG()">Next</button>
    navigation = """
        <div class="steps">
    """

    # Embedding the SVGs
    svg_content = ""
    for svg_file in svg_files:
        svg_rel_path = os.path.relpath(svg_file)
        svg_content += f'        <object type="image/svg+xml" data="./{svg_rel_path}"></object>\n'

    # HTML navigation script
    script = """
        </div>
        <script>
            const svgs = document.querySelectorAll('.steps > object');
            let current = 0;

            function showSVG(index) {
                svgs.forEach((svg, i) => {
                    if (i === index) {
                        svg.style.opacity = 1; // Show current SVG
                    } else {
                        svg.style.opacity = 0; // Hide other SVGs
                    }   
                });
            }

            function nextSVG() {
                console.log('next');
                current = (current + 1) % svgs.length;
                showSVG(current);
            }

            function previousSVG() {
                console.log('prev');
                current = (current - 1 + svgs.length) % svgs.length;
                showSVG(current);
            }

            showSVG(current);

            document.addEventListener('keydown', function(event) {
                switch (event.key) {
                    case 'j':
                        nextSVG();
                        break;
                    case 'k':
                        previousSVG();
                        break;
                    case 'g':
                        current = 0;
                        showSVG(current);
                        break;
                    case 'G':
                        current = svgs.length - 1;
                        showSVG(current);
                        break;
                }
            });

        </script>
        </body>
        </html>
    """

    # Combining all parts
    html_content = head + navigation + svg_content + script

    # Saving the HTML file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as file:
        file.write(html_content)

    return f"HTML page created at {output_path}"


