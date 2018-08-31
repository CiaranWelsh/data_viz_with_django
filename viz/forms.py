from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Dct

GENES = ['ACTA2', 'ADAMTS1', 'ATP6AP1', 'B2M', 'BGN', 'BHLHE40',
         'CAV1', 'CDKN2A', 'CDKN2B', 'COL1A1', 'COL1A2', 'COL4A1',
         'COL5A1', 'CTGF', 'DCN', 'EGR2', 'ELN', 'ENG', 'ETS1',
         'FBLN1', 'FBN1', 'FGF2', 'FN1', 'FOSB', 'GADD45B', 'GUSB',
         'HAS2', 'ID1', 'IL1A', 'IL1B', 'IL6', 'ITGA1', 'ITGA2',
         'JUN', 'JUNB', 'LARP6', 'LOXL1', 'LOXL2', 'LTBP2', 'MMP1',
         'MMP13', 'MMP14', 'MMP2', 'NOX4', 'PDGFA', 'PMEPA1',
         'PPIA', 'PPP3CA', 'PSMD14', 'PTEN', 'RARA', 'RARG', 'RHOB',
         'SERPINE1', 'SERPINE2', 'SKI', 'SKIL', 'SMAD3', 'SMAD7',
         'SPARC', 'TGFB1', 'TGFBR1', 'TGFBR2', 'THBS1', 'THBS2',
         'TIMP1', 'TIMP3', 'TP53BP1', 'VCAN', 'VEGFA', 'VIM']

GENES = [(i, i) for i in GENES]

TIMEPOINTS = [0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]
TIMEPOINTS = [(i, i) for i in TIMEPOINTS]

# REPLICATES = range(1, 7)


TREATMENTS = ['TGFb', 'Control']
TREATMENTS = [(i, i) for i in TREATMENTS]

CELL_LINES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
CELL_LINES = [(i, i) for i in CELL_LINES]

REPLICATES = [(i, i) for i in [1, 2, 3, 4, 5, 6]]


class DBControllerForm(forms.Form):

    checkbox_classes = 'form-check-input'

    genes = forms.MultipleChoiceField(
        choices=GENES,
        initial=['ACTA2']
    )
    genes.widget.attrs.update({'class': 'custom-select',
                               'multiple': 'multiple',
                               'name': 'genes_dropdown'})
    # genes.widget.attrs.update({
    #     'size': 27,
    # })

    cell_lines = forms.MultipleChoiceField(
        choices=CELL_LINES,
        widget=forms.CheckboxSelectMultiple,
        initial=['A', 'D', 'G'],
    )
    cell_lines.widget.attrs.update({'class': checkbox_classes})

    treatments = forms.MultipleChoiceField(
        choices=TREATMENTS,
        widget=forms.CheckboxSelectMultiple,
        initial=['TGFb']
    )
    treatments.widget.attrs.update({'class': checkbox_classes})

    time_points = forms.MultipleChoiceField(
        choices=TIMEPOINTS,
        widget=forms.CheckboxSelectMultiple,
        initial=[0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]
    )
    time_points.widget.attrs.update({'class': checkbox_classes})


class PCAForm(forms.Form):
    checkbox_classes = 'form-check-input'

    cell_lines = forms.MultipleChoiceField(
        choices=CELL_LINES,
        widget=forms.CheckboxSelectMultiple,
        initial=list('ABDCEFGHI'),
    )
    cell_lines.widget.attrs.update({'class': checkbox_classes})

    time_points = forms.MultipleChoiceField(
        choices=TIMEPOINTS,
        widget=forms.CheckboxSelectMultiple,
        initial=[0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]
    )
    time_points.widget.attrs.update({'class': checkbox_classes})


    replicates = forms.MultipleChoiceField(
        choices=REPLICATES,
        widget=forms.CheckboxSelectMultiple,
        initial=[1, 2, 3, 4, 5, 6]
    )

    treatments = forms.MultipleChoiceField(
        choices=TREATMENTS + [('Baseline', 'Baseline')],
        widget=forms.CheckboxSelectMultiple,
        initial=['TGFb', 'Baseline', 'Control']
    )
    colour_by = forms.MultipleChoiceField(
        choices=[
            ('cell_lines', 'cell_lines'),
            ('treatments', 'treatments'),
            ('time_points', 'time_points'),
            ('replicates', 'replicates'),
        ],
        widget=forms.CheckboxSelectMultiple,
        initial=['cell_lines']
    )


class PCAExplainedVarForm(forms.Form):
    pass
