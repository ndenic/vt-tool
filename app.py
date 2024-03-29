import os

from flask import Flask, request, render_template, send_file
from services.visual_comparison import compare_images, get_diff_percent

app = Flask(__name__,  template_folder='static/templates/')
app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url1 = request.form['url1']
        url2 = request.form['url2']
        threshold = float(request.form['threshold'])
        test_name = request.form['test_name']
        image_folder = f'static/images/{test_name}/'
        result_folder = f'static/images/{test_name}/'
        diff = None

        # Create dir
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        driver.get(url1)
        driver.save_screenshot(f'{image_folder}{test_name}-img1.png')
        driver.get(url2)
        driver.save_screenshot(f'{image_folder}{test_name}-img2.png')
        driver.quit()

        # Compare images
        diff = compare_images(f'{test_name}-img1.png', f'{test_name}-img2.png', image_folder, result_folder,
                              threshold)
        diff_percent = get_diff_percent(f'{test_name}-img1.png', f'{test_name}-img2.png', image_folder, threshold)

        return render_template('/results.html', diff=diff, diff_percent=diff_percent, test_name=test_name)

    return render_template('/index.html')


@app.route('/images/<test_name>', methods=['GET'])
def image_explorer(test_name):
    images_dir = os.path.join(app.config['UPLOAD_FOLDER'], test_name)
    if not os.path.exists(images_dir):
        return f"No images found for test '{test_name}'"
    images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    return render_template('/image_explorer.html', images=images, test_name=test_name)


@app.route('/download_diff/<test_name>')
def download_diff(test_name):
    image_folder = f'static/images/{test_name}/'
    return send_file(os.path.join(image_folder, 'result.png'), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
