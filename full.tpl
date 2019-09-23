{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}


{%- block header -%}
<!DOCTYPE html>
<html>
<head>
{%- block html_head -%}
<meta charset="utf-8" />
{% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
<title>{{nb_title}}</title>
<!-- This is a test - new test -->

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

{% block ipywidgets %}
{%- if "widgets" in nb.metadata -%}
<script>
(function() {
  function addWidgetsRenderer() {
    var mimeElement = document.querySelector('script[type="application/vnd.jupyter.widget-view+json"]');
    var scriptElement = document.createElement('script');
    var widgetRendererSrc = '{{ resources.ipywidgets_base_url }}@jupyter-widgets/html-manager@*/dist/embed-amd.js';
    var widgetState;

    // Fallback for older version:
    try {
      widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);

      if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {
        widgetRendererSrc = '{{ resources.ipywidgets_base_url }}jupyter-js-widgets@*/dist/embed.js';
      }
    } catch(e) {}

    scriptElement.src = widgetRendererSrc;
    document.body.appendChild(scriptElement);
  }

  document.addEventListener('DOMContentLoaded', addWidgetsRenderer);
}());
</script>
{%- endif -%}
{% endblock ipywidgets %}

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<!-- Custom Stylesheet for exports -->
<style type='text/css'>
div#notebook {
  padding: 0px;
}
div.input {
  padding: 0.3em;
}
h1 {
    font-family: sans-serif;
    font-variant: small-caps;
    border-bottom: 1px solid black;
    margin-top: 0.1em!important;
}
h2 {
    font-size: 1.2em !important;
    margin-left: 1em !important;
    margin-top: 0.8em !important;
}
h3 {
    font-size: 1.1em !important;
    font-weight: normal !important;
    /*margin: 0.4em !important;*/
    margin-left: 1em !important;
}
p {
    margin-left: 1em;
    margin-top: 0.5em !important;
}
p, h2, h3, li, ul, ol, table {
    font-family: serif;
}
.page {
      position: relative;
}
.ttlpage-title {
    text-align: center;
    border: 2px solid black;
    border-left: none;
    border-right: none;
    padding: 1em;
    margin-bottom: 3em !important;
}
.ttlpage-heading {
    font-size: 2em;
    font-family: serif;
    text-align: center !important;
    width: 100%;
}
.ttlpage-instructor {
    font-size: 1em;
    font-family: serif;
    text-align: center !important;
    width: 100%;
}
.title-page {
    padding-top: 15em;
}
.title-page p,.title-page h1 {
    margin-left: 0 !important;
}
.pg-header-container {
    position: absolute;
    margin: 0;
    top: 0;
    left: 0;
    right: 0;
    padding-right: 1em;
    padding-left: 0.5em;
    border-bottom: 2px solid gray !important;
    color: gray !important;
}
.pg-header {
    top: 0;
    left: 0;
    right: 0;
    position: relative;
}
.pg-header table {
    width: 100%;
}
.pg-footer p {
    text-align: center;
}
.rightalign {
    text-align: right !important;
}
.leftalign {
    text-align: left !important;
}
.center {
    width: 100%;
    text-align: center !important;
}
.section-header {
    font-family: sans-serif;
    font-variant: small-caps;
    border-bottom: 1px solid black;
}
.output_png.output_subarea {
    margin-left: auto;
    margin-right: auto;
}
@media only print {
      .page {
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100vw;
        height: 100vh;
        page-break-before: always;
        page-break-after: auto;
        margin: 0;
        padding: 0;
    }
    .pg-spacer {
      width: 100%;
      min-height: 1.5em;
    }
    .pg-footer {
        bottom: 1em;
        left: 0;
        right: 0;
        position: absolute;
    }
    .code_cell .inner_cell {
        margin-left: 1em !important;
    }
    div.prompt {
        display: none;
    }
    div.lab-text {
        margin-left: 0em;
    }
}
@page {
   @bottom-right {
    content: counter(page) " of " counter(pages);
   }
}


</style>


<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}

div#notebook {
  overflow: visible;
  border-top: none;
}

{%- if resources.global_content_filter.no_prompt-%}
div#notebook-container{
  padding: 6ex 12ex 8ex 12ex;
}
{%- endif -%}

@media print {
  div.cell {
    display: block;
    page-break-inside: avoid;
  } 
  div.output_wrapper { 
    display: block;
    page-break-inside: avoid; 
  }
  div.output { 
    display: block;
    page-break-inside: avoid; 
  }
}
</style>

<!-- Custom stylesheet, it must be in the same directory as the html file -->
<link rel="stylesheet" href="custom.css">

<!-- Loading mathjax macro -->
{{ mathjax() }}
{%- endblock html_head -%}
</head>
{%- endblock header -%}

{% block body %}

<body>
  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
      <div class='page'>
{{ super() }}
        <div class='pg-footer'>
        <p>Page {{ page.number }}</p>
        </div>
      </div>
    </div>
  </div>
</body>
{%- endblock body %}

{% set pgheader = namespace(source='') %}
{% set page = namespace(number=0) %}
{% set listings = namespace(count=1) %}
{% set figures = namespace(count=1) %}

{% block input_group -%}
{{ super() }}
{% if 'listing' in cell['metadata'].get('tags', []) %}
  <p class='center'><b>Listing {{ listings.count }}: </b>
    {{ cell['metadata'].get('description', '') }}
  </p>
  {% set listings.count = listings.count + 1 %}
{% endif %}
{% endblock input_group %}

{% block output_group %}
{{ super() }}
{% if 'figure' in cell['metadata'].get('tags', []) %}
  <p class='center'><b>Figure {{ figures.count }}: </b>
    {{ cell['metadata'].get('description', '') }}
  </p>
  {% set figures.count = figures.count + 1 %}
{% endif %}
{% endblock output_group %}


{% block any_cell %}
  {% if 'pgheader' in cell['metadata'].get('tags', []) %}
    {% set pgheader.source = cell['source'] %}
  {% elif 'newpage' in cell['metadata'].get('tags', []) %}
      {% if page.number > 0 %}
      <div class='pg-footer'>
      <p>Page {{ page.number }}</p>
      </div>
      {% endif %}
      </div>
      <div class='page'>
        <div class='pg-header-container'>
          {{ pgheader.source }}
        </div>
        <div class='pg-spacer'></div>
        {% set page.number = page.number + 1 %}
  {% else %}
      {{ super() }}
  {% endif %}
{% endblock any_cell %}

{% block footer %}
{{ super() }}
</html>
{% endblock footer %}
