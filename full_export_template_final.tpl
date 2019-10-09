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
<script>
function page_setup() {
    $('div.page#pg-num-' + $('#page_count').val()).addClass('last');
    pagecount = parseInt($('#page_count').val());
    toc_html = '';
    for (var i = 1; i <= pagecount; i++) {
        pg_elements = document.querySelectorAll('.h-pg-' + i);
        for (var el = 0; el < pg_elements.length; el++) {
            toc_html += '<div class="contents-line ' + (pg_elements[el].tagName == 'H2' ? 'indented' : '') + '"><div class="leftalign">' + pg_elements[el].innerText + '</div><div class="rightalign">' + i + '</div></div>';
        }
    }
    $('#pg-contents').html(toc_html);
}

$(document).ready(page_setup);

</script>

<style type='text/css'>
div#notebook {
  padding: 0px;
}
div.input {
  padding: 0.3em;
}
.rendered_html img, .rendered_html svg {
    width: 50%;
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
.page.last {
    height: 99vh !important;
    top: 0;
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
    padding-left: 2em;
    padding-right: 2em;
}
.title-page p,.title-page h1 {
    margin-left: 0 !important;
}
.pg-header-container {
    border-bottom: 2px solid gray !important;
    color: gray !important;
    display: none;
}
.pg-header table {
    width: 100%;
}
.pg-footer {
  display: none;
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
.contents-line {
    border-bottom: dotted black 2px;
    margin-bottom: 1em;
    padding-right: 1em;
}
.contents-line div {
    display: inline-block;
    width: 50%;
}
.contents-line.indented {
    margin-left: 2em;
}
.page.contents {
    margin-left: 7em;
    padding-right: 1em;
    padding-top: 4em;
}
.page.contents h1 {
    text-align: center;
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
    .page.contents {
        margin-left: 1em;
    }
    .pg-spacer {
      width: 100%;
      min-height: 1.5em;
    }
    .pg-header-container {
        display: block;
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
    .pg-footer {
        display: block;
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

{% set pagehtml = namespace(source='') %}
{% set pgheader = namespace(source="<div class='pg-header'>
    <table>
        <tr>
            <td><p class='leftalign'>" + nb.metadata.get('title', '') + "</p></td>
            <td><p class='rightalign'>" + nb.metadata.get('author', '') + "</p></td>
        </tr>
    </table>
</div>") %}
{% set page = namespace(number=1) %}
{% set listings = namespace(count=1) %}
{% set figures = namespace(count=1) %}

{% block body %}

<body>
  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
      <div class='page'>
        <div class='title-page'>
          <p  class='ttlpage-heading'>{{ nb.metadata.get('class', '') }}</p>
          <p class='ttlpage-heading'>{{ nb.metadata.get('class_code', '') }}</p>
          <p class='ttlpage-instructor'>{{ nb.metadata.get('instructor', '') }}</p>
          <h1 class='ttlpage-title'>{{ nb.metadata.get('title', '') }}</h1>
          <p class='rightalign'><em>Submitted by:</em></p>
          <p class='rightalign'>{{ nb.metadata.get('author', '') }}</p>
          <p class='rightalign'>{{ nb.metadata.get('date', '') }}</p>
        </div>
      </div>
      <div class='page contents'>
        <h1>Contents</h1>
        <div id='pg-contents'>
        
        </div>
      </div>
      <div class='page' id='pg-num-{{ page.number }}'>
        <div class='pg-header-container'>
          {{ pgheader.source }}
        </div>
      <div class='pg-spacer'></div>
      {# Load the entire page contents, populating the listings and headers index #}
      {% set pagehtml.source = super() %}
      {{ pagehtml.source|replace("[PAGE_COUNT]", page.number) }}
        
        <div class='pg-footer'>
        <p>Page {{ page.number }} of {{ page.number }}</p>
        </div>
      </div>
    </div>
  </div>
  <input type='hidden' id='page_count' value='{{ page.number }}'/>
</body>
{%- endblock body %}

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
  {% if 'newpage' in cell['metadata'].get('tags', []) %}
        <div class='pg-footer'>
        <p>Page {{ page.number }} of [PAGE_COUNT]</p>
        </div>
        </div>
      {% set page.number = page.number + 1 %}
      <div class='page' id='pg-num-{{ page.number }}'>
        <div class='pg-header-container'>
          {{ pgheader.source }}
        </div>
        <div class='pg-spacer'></div>
  {% else %}
      {{ super()|replace("<h1>", "<h1 class='h-pg-" ~ page.number ~ "'>")|replace("<h2>", "<h2 class='h-pg-" ~ page.number ~ "'>") }}
  {% endif %}
{% endblock any_cell %}

{% block footer %}
{{ super() }}
</html>
{% endblock footer %}
