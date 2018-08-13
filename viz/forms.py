from django import forms
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

GENES = [(i.lower(), i) for i in GENES]

TIMEPOINTS = [0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]

REPLICATES = range(1, 7)

TREATMENTS = ['TGFb', 'Control']

CELL_LINES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

class NewForm(forms.Form):
    name = forms.CharField(label='your name', max_length=100)



#
# class DctModelForm(forms.ModelForm):
#
#     class Meta:
#         model = Dct
#         fields = ['time', 'replicate', 'treatment', 'gene', 'cell_line']
#
#         widgets = {
#             'gene': forms.SelectMultiple(choices=enumerate(GENES), attrs={'id': 'gene_selection'}),
#             'time': forms.CheckboxSelectMultiple(choices=enumerate(TIMEPOINTS), attrs={'id': 'time_selection'}),
#             'replicate': forms.CheckboxSelectMultiple(choices=enumerate(REPLICATES), attrs={'id': 'replicate_selection'}),
#             'treatment': forms.CheckboxSelectMultiple(choices=enumerate(TREATMENTS), attrs={'id': 'treatments_selection'}),
#             'cell_line': forms.CheckboxSelectMultiple(choices=enumerate(CELL_LINES), attrs={'id': 'cell_lines_selection'})
#         }


class GenesForm(forms.Form):
    gene = forms.MultipleChoiceField(
        choices=GENES,
        label=False
    )#, attrs={'id': 'gene_form'})

    gene.widget.attrs.update({
        'size': 15,
    })

    # class Meta:
    #     model = Dct
    #     fields = ['time', 'replicate', 'treatment', 'gene', 'cell_line']
    #
    #     widgets = {
    #         'gene': forms.SelectMultiple(choices=enumerate(GENES), attrs={'id': 'gene_selection'}),
    #     }













