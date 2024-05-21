from flask import Flask, render_template, request, redirect, url_for, send_file
import dropbox
import os
from io import BytesIO
from flask import Flask, send_file
app = Flask(__name__)

dropbox_access_token = "sl.B1dp1sYT_qfoNiy-1rAijcqKOiaJtgbwfRbSNnZrhLhQ0SQnzLCbJtTYScwDfl4ADeqdfpzt6PuRt_gsxgHOw456ptX87CEFffdBcCid987mJyD9i2SU8tHuQ8PzSa9X9oosNHHaNZhl"
dbx = dropbox.Dropbox(dropbox_access_token)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filename = file.filename
    print(filename)
    temp_file_path = os.path.join("temp", filename)  # Temporarily save file locally
    file.save(temp_file_path)
    dropbox_path = "/image/cloud/" + filename

    with open(temp_file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path)

    os.remove(temp_file_path)  # Remove temporary file

    return "File uploaded successfully"

@app.route('/list')
def list_files():
    files = []
    for entry in dbx.files_list_folder('/image/cloud').entries:
        files.append(entry.name)
    return render_template('list.html', files=files)
    


from flask import send_file
from io import BytesIO

@app.route('/download/<filename>')
def download_file(filename):
    dropbox_path = "/image/cloud/" + filename
    _, res = dbx.files_download(dropbox_path)
    data = res.content

    # Create a BytesIO object to hold the file content
    file_obj = BytesIO(data)
    
    # Send the file to the client for download
    return send_file(
        file_obj,
        as_attachment=True,
        download_name=filename,
        mimetype='application/octet-stream'  # Set the MIME type explicitly
    )


@app.route('/delete/<filename>')
def delete_file(filename):
    dropbox_path = "/image/cloud/" + filename
    dbx.files_delete_v2(dropbox_path)
    return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(debug=True)
