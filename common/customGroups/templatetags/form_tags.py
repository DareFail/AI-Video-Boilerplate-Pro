from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_form_fields(form):
    rendered_values = [render_field(form[field]) for field in form.fields]
    return mark_safe("".join(rendered_values))


@register.simple_tag
def render_field(form_field):
    render_function = {
        "select": render_select_input,
        "checkbox": render_checkbox_input,
        "date": render_date_input,
        "datetime": render_datetime_input,
    }.get(form_field.widget_type, render_text_input)
    return render_function(form_field)


@register.simple_tag
def render_text_input(form_field):
    TEXT_INPUT_TEMPLATE = """<div class="mb-3">
      <label for="{{ form_field.id_for_label }}" class="form-label">{{ form_field.label }}</label>
      {{ form_field }}
      <small class="form-text text-muted">{{ form_field.help_text }}</small>
      {{ form_field.errors }}
    </div>
    """
    return _render_field(TEXT_INPUT_TEMPLATE, form_field)


@register.simple_tag
def render_date_input(form_field):
    TEXT_INPUT_TEMPLATE = """<div class="mb-3">
      <label for="{{ form_field.id_for_label }}" class="form-label">{{ form_field.label }}</label>
      {% if form_field.value %}
        <input type="date" name="{{ form_field.name }}" id="{{ form_field.id_for_label }}" value="{{ form_field.value|date:"Y-m-d" }}">
      {% else %}
        <input type="date" name="{{ form_field.name }}" id="{{ form_field.id_for_label }}" value="">
      {% endif %}
      <small class="form-text text-muted">{{ form_field.help_text }}</small>
      {{ form_field.errors }}
    </div>
    """
    return _render_field(TEXT_INPUT_TEMPLATE, form_field)


@register.simple_tag
def render_select_input(form_field):
    SELECT_INPUT_TEMPLATE = """<div class="mb-3">
      <label for="{{ form_field.id_for_label }}" class="form-label">{{ form_field.label }}</label>
      {{ form_field }}
      <small class="form-text text-muted">{{ form_field.help_text }}</small>
      {{ form_field.errors }}
    </div>
    """
    return _render_field(SELECT_INPUT_TEMPLATE, form_field)


@register.simple_tag
def render_checkbox_input(form_field):
    CHECKBOX_INPUT_TEMPLATE = """
    <div class="mb-3">
      <div class="form-check">
        {{ form_field }}
        <label class="form-check-label" for="flexCheckChecked">
          {{ form_field.label }}
        </label>
      </div>
      <small class="form-text text-muted">{{ form_field.help_text }}</small>
      {{ form_field.errors }}
    </div>
    """
    return _render_field(CHECKBOX_INPUT_TEMPLATE, form_field)

@register.simple_tag
def render_datetime_input(form_field):
    DATETIME_INPUT_TEMPLATE = """<div class="mb-3">
      <label for="{{ form_field.id_for_label }}" class="form-label">{{ form_field.label }}</label>
      {% if form_field.value %}
        <input type="datetime-local" name="{{ form_field.name }}" id="{{ form_field.id_for_label }}" value="{{ form_field.value|date:"Y-m-d\\TH:i" }}">
      {% else %}
        <input type="datetime-local" name="{{ form_field.name }}" id="{{ form_field.id_for_label }}" value="">
      {% endif %}
      <small class="form-text text-muted">{{ form_field.help_text }}</small>
      {{ form_field.errors }}
    </div>
    """
    return _render_field(DATETIME_INPUT_TEMPLATE, form_field)

def _render_field(template_text, form_field):
    template_object = template.Template(template_text)
    context = template.Context({"form_field": form_field})
    return template_object.render(context)
