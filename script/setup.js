function create_element(name, attributes) {
    var element = document.createElement(name);
    for (let key in attributes) {
        element.setAttribute(key, attributes[key]);
    }
    return element;
}

function create_script(src, attributes) {
    attributes = attributes || {};
    attributes.src = src
    var script = create_element('script', attributes);
    document.head.insertBefore(script, document.head.firstChild);
}

function create_style(src) {
    var style = create_element('link', {
        'rel': 'stylesheet',
        'href': src
    });
    document.head.insertBefore(style, document.head.firstChild);
}

function init_ga() {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-155995840-1');
}

function init_hljs() {
    if (typeof hljs != 'undefined') {
        document.querySelectorAll('code').forEach((block) => {
            hljs.highlightBlock(block);
        });
    }
}

function init_videos() {
    var videos = document.getElementsByClassName('video');
    for(var i = 0; i < videos.length; i++) {
        var video = videos.item(i);
        var iframe = create_element('iframe', {
            'src': 'https://www.youtube.com/embed/' + video.getAttribute('data-video-id'),
            'frameborder': '0',
            'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
            'allowFullScreen': ''
        });
        video.appendChild(iframe);
    }
}

function init_mailchimp() {
    window.dojoRequire(["mojo/signup-forms/Loader"], function(L) {
        L.start({
            "baseUrl": "mc.us4.list-manage.com",
            "uuid":"db9cdab3c81c5706fb0ede08a",
            "lid":"44f897bb92",
            "uniqueMethods":true
        })
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    var raw_content = document.body.getAttribute('data-content') || '';
    var content = raw_content.split(';');

    create_script('https://www.googletagmanager.com/gtag/js?id=UA-155995840-1', {
        'async': '',
        'onload': 'init_ga()'
    });

    if (content.includes('code')) {
        create_script('/script/highlight.pack.js', {
            'async': '',
            'onload': 'init_hljs()'
        });
        create_style('/style/color-brewer.css');
    }

    if (content.includes('figures')) {
        create_style('/style/figures.css');
    }

    if (content.includes('video')) {
        init_videos();
    }

    if (!content.includes('sub')) {
        create_script(
            'https://downloads.mailchimp.com/js/signup-forms/popup/unique-methods/embed.js', {
            'data-dojo-config': 'usePlainJson: true, isDebug: false',
            'async': '',
            'onload': 'init_mailchimp()'
        });
    }
});

