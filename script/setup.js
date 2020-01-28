// Initialize google analytics
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-155995840-1');

// Initialize higlight.js
document.addEventListener('DOMContentLoaded', (event) => {
    if (typeof hljs != 'undefined') {
        document.querySelectorAll('code').forEach((block) => {
            hljs.highlightBlock(block);
        });
    }
});
