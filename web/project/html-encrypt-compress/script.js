// Fungsi untuk menghapus line breaks, tabs, dan spasi ganda (Compress)
function compressHTML(html) {
    return html
        .replace(/\n/g, '')          
        .replace(/[\t ]+\</g, '<')   
        .replace(/\>[\t ]+\</g, '><') 
        .replace(/\>[\t ]+$/g, '>')  
        .replace(/\s+/g, ' ')        
        .trim();
}

// Fungsi Full Encoding khusus untuk dicocokkan dengan unescape()
function encodeForUnescape(str) {
    let encoded = '';
    for (let i = 0; i < str.length; i++) {
        let hex = str.charCodeAt(i).toString(16).toUpperCase();
        if (hex.length <= 2) {
            encoded += '%' + hex.padStart(2, '0');
        } else {
            // Menangani karakter khusus/unicode
            encoded += '%u' + hex.padStart(4, '0');
        }
    }
    return encoded;
}

// Fungsi untuk menyatukan HTML yang sudah dienkode ke dalam Template Full HTML
function encryptHTML(html, title) {
    // 1. Full Encode HTML Asli
    const encoded = encodeForUnescape(html);
    
    // 2. Gabungkan dengan kerangka utama
    const template = `<!DOCTYPE html>
<!-- 
        __   
       /  \\      
       |  |
       |  |
     __|  |__
    /  |  |  \\__ 
  __|  |  |  |  |
 /  /        |  |
 |              |
 \\              |
  \\             /
   \\___________/
     FUCK You!
--><html><head><title>${title}</title><meta property="og:title" content="mnytc"> <meta property="og:type" content="website"> <meta name="viewport" content="width=device-width, initial-scale=1"> <meta property="og:url" content="https://www.mnytc.eu"><meta property="og:image" content="https://cdn.mnytc.eu/monytccc-black.png"><meta name="description" content="mnytc is a shared web hosting service for software development projects that uses a mnytc version control system and an internet hosting service. It is widely used for computer code. It provides access control and several collaboration features such as bug tracking, feature requests, task management, and websites for each project."><meta property="og:description" content="mnytc is a shared web hosting service for software development projects that uses a mnytc version control system and an internet hosting service. It is widely used for computer code. It provides access control and several collaboration features such as bug tracking, feature requests, task management, and websites for each project."><meta property="og:site_name" content="mnytc"> <meta property="fb:app_id" content="123456789"><link rel="apple-touch-icon" sizes="180x180" href="https://cdn.mnytc.eu/apple-touch-icon.png"><link rel="icon" type="image/png" sizes="32x32" href="https://cdn.mnytc.eu/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="https://cdn.mnytc.eu/favicon-16x16.png"><link rel="manifest" href="/site.webmanifest"><link rel="mask-icon" href="https://cdn.mnytc.eu/safari-pinned-tab.svg" color="#5bbad5"><meta name="msapplication-TileColor" content="#da532c"><meta name="theme-color" content="#ffffff"><link rel="shortcut icon" href="https://cdn.mnytc.eu/mnytc.png" type="image/x-icon"> </head><body><script type="text/javascript"><!--
document.write(unescape('${encoded}'));
//--><\/script></body></html>`;

    return template;
}

// --- Event Listeners untuk Tombol ---

document.getElementById('btnCompress').addEventListener('click', () => {
    const input = document.getElementById('inputHtml').value;
    document.getElementById('outputHtml').value = compressHTML(input);
});

document.getElementById('btnEncrypt').addEventListener('click', () => {
    const input = document.getElementById('inputHtml').value;
    const title = document.getElementById('pageTitle').value || 'HOME - mnytc';
    document.getElementById('outputHtml').value = encryptHTML(input, title);
});

document.getElementById('btnCompressEncrypt').addEventListener('click', () => {
    const input = document.getElementById('inputHtml').value;
    const title = document.getElementById('pageTitle').value || 'HOME - mnytc';
    
    const compressed = compressHTML(input);
    document.getElementById('outputHtml').value = encryptHTML(compressed, title);
});

// Fitur Copy
document.getElementById('btnCopy').addEventListener('click', () => {
    const output = document.getElementById('outputHtml');
    output.select();
    document.execCommand('copy');
    alert('Kode berhasil disalin!');
});