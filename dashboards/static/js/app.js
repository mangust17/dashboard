const container = document.getElementById('dash-container');
const dashAppUrl = 'http://127.0.0.1:8050';  // Замените на URL вашего Dash-приложения

const iframe = document.createElement('iframe');
iframe.src = dashAppUrl;
iframe.style.width = '100%';
iframe.style.height = '600px';  // Установите высоту по вашему усмотрению

container.appendChild(iframe);