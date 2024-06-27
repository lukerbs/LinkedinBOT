import markdown
import pdfkit
import os

from .ai import chatgpt



# Convert Markdown to HTML
html_content = markdown.markdown(markdown_content)

# Save the HTML content to a temporary file
with open('temp.html', 'w') as f:
    f.write(html_content)

# Convert HTML to PDF
pdfkit.from_file('temp.html', 'output.pdf')

# Clean up the temporary HTML file

os.remove('temp.html')

print('PDF generated successfully!')