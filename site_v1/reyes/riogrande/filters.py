import django_filters
import sys 
# from django_filters.widgets import RangeWidget
from django_filters import widgets as filter_widgets
from django.forms import widgets as form_widgets
from datetime import date, datetime

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models


labels = {
    'dat': {
        'gt': 'Min',
        'lt': 'Max',
        'group': 'Date',
        'placeholder': 'e.g. 2021-06-28'
    },
    'rm': {
        'gt': 'Downstream Min',
        'lt': 'Upstream Max',
        'group': 'River Mile',
        'placeholder': 'e.g. 78.5'
    },
    'sum_len': {
        'gt': 'Min',
        'lt': 'Max',
        'group': 'Percent Dry',
        'placeholder': 'e.g. 50%'
    },
    'frac_len': {
        'gt': 'Min',
        'lt': 'Max',
        'group': 'Dry Length (River Miles)',
        'placeholder': 'e.g. 10.5'
    },
    'dry_len': {
        'gt': 'Min',
        'lt': 'Max',
        'group': 'Dry Length',
        'placeholder': 'e.g. 10.5'
    },
    'flow_cfs': {
        'gt': 'Min',
        'lt': 'Max',
        'group': 'Streamflow',
        'placeholder': 'e.g. 16.34'
    },
    'latitude': {
        'gt': 'Xmin',
        'lt': 'Xmax',
        'group': 'Latitude',
        'placeholder': 'e.g. 35.06'
    },
    'longitude': {
        'gt': 'Ymin',
        'lt': 'Ymax',
        'group': 'Longitude',
        'placeholder': 'e.g. -106.65'
    },
    'feature': {
        'group': 'Feature Name',
        'icontains': 'Contains',
        'placeholder': 'e.g. USGS'
    },
    'prov_flag': {
        'group': 'Data Qualifier',
        'icontains': 'Contains',
        'placeholder': 'e.g. P'
    },
    'usgs_id': {
        'group': 'Streamgage',
        'label' : 'USGS ID',
        'choices': ('usgs_id', 'usgs_feature_display_name'),
    },

    
}

class GroupedFilterSetMixin:
    def grouped_filters(self):
        grouped = {}
        for name, f in self.filters.items():
            group = getattr(f, 'group', None)
            if group:
                if group not in grouped:
                    grouped[group] = []
                grouped[group].append((name, f))
        return grouped

class GroupedFilterMixin:
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)

class GroupedCharFilter(GroupedFilterMixin, django_filters.CharFilter):
    pass

class GroupedDateFilter(GroupedFilterMixin, django_filters.DateFilter):
    pass

class GroupedChoiceFilter(GroupedFilterMixin, django_filters.ChoiceFilter):
    pass

class GroupedBooleanFilter(GroupedFilterMixin, django_filters.BooleanFilter):
    pass

class GroupedNumberFilter(GroupedFilterMixin, django_filters.NumberFilter):
    pass

class GroupedRangeFilter(GroupedFilterMixin, django_filters.RangeFilter):
    pass

class GroupedDateTimeFilter(GroupedFilterMixin, django_filters.DateTimeFilter):
    pass

class GroupedTimeFilter(GroupedFilterMixin, django_filters.TimeFilter):
    pass

class GroupedModelChoiceFilter(GroupedFilterMixin, django_filters.ModelChoiceFilter):
    pass

class GroupedModelMultipleChoiceFilter(GroupedFilterMixin, django_filters.ModelMultipleChoiceFilter):
    pass

class GroupedMultipleChoiceFilter(GroupedFilterMixin, django_filters.MultipleChoiceFilter):
    pass

class GroupedNumericRangeFilter(GroupedFilterMixin, django_filters.NumericRangeFilter):
    pass

class GroupedUUIDFilter(GroupedFilterMixin, django_filters.UUIDFilter):
    pass

class GroupedAllValuesFilter(GroupedFilterMixin, django_filters.AllValuesFilter):
    pass

class GroupedAllValuesMultipleFilter(GroupedFilterMixin, django_filters.AllValuesMultipleFilter):
    pass


class DrySegFilter(GroupedFilterSetMixin, django_filters.FilterSet):
    
    # dates
    field_lookup_label = ['dat', 'gt', 'dat']
    dat__gt = GroupedDateFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.DateInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[1] = 'lt'
    dat__lt = GroupedDateFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.DateInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    # dry lengths
    field_lookup_label = ['dry_length', 'gt', 'dry_len']
    dry_length__gt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[1] = 'lt'
    dry_length__lt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    # rms
    field_lookup_label = ['rm_down', 'gt', 'rm']
    rm_down__gt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[0] = 'rm_up'
    field_lookup_label[1] = 'lt'
    rm_up__lt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))

    class Meta:
        model = models.DryLengthAgg 
        fields = ("dat", "dry_length", "rm_up", "rm_down")  

class FeatureFilter(GroupedFilterSetMixin, django_filters.FilterSet):
    # feature
    field_lookup_label = ['feature', 'icontains', 'feature']
    feature = GroupedCharFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                # widget=filter_widgets.Ch(
                                #     attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
                                    )

    # rms
    field_lookup_label = ['rm', 'gt', 'rm']
    rm__gt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[1] = 'lt'
    rm__lt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))

    class Meta:
        model = models.FeatureRm
        fields = ("feature", "rm__gt", "rm__lt" )

class DryLenFilter(GroupedFilterSetMixin, django_filters.FilterSet):
    # Define date filters
    field_lookup_label = ['dat', 'gt', 'dat']
    dat__gt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    field_lookup_label[1] = 'lt'
    dat__lt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    # Define dry length filters for 'isleta, agnostura, acacia, and combined'
    field_lookup_label = ['isleta_sum_len', 'gt', 'sum_len']
    isleta_sum_len__gt = GroupedNumberFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label='Isleta: ' + labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    isleta_sum_len__lt = GroupedNumberFilter(
        field_name='isleta_sum_len', lookup_expr='lt',
        label='Isleta: ' + labels['sum_len']['lt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    isleta_frac_len__gt = GroupedNumberFilter(
        field_name='isleta_frac_len', lookup_expr='gt',
        label='Isleta: ' + labels['frac_len']['gt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )
    isleta_frac_len__lt = GroupedNumberFilter(
        field_name='isleta_frac_len', lookup_expr='lt',
        label='Isleta: ' + labels['frac_len']['lt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )

    # Acacia dry length filters
    acacia_sum_len__gt = GroupedNumberFilter(
        field_name='acacia_sum_len', lookup_expr='gt',
        label='Acacia: ' + labels['sum_len']['gt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    acacia_sum_len__lt = GroupedNumberFilter(
        field_name='acacia_sum_len', lookup_expr='lt',
        label='Acacia: ' + labels['sum_len']['lt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    acacia_frac_len__gt = GroupedNumberFilter(
        field_name='acacia_frac_len', lookup_expr='gt',
        label='Acacia: ' + labels['frac_len']['gt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )
    acacia_frac_len__lt = GroupedNumberFilter(
        field_name='acacia_frac_len', lookup_expr='lt',
        label='Acacia: ' + labels['frac_len']['lt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )

    # Angostura dry length filters
    angostura_sum_len__gt = GroupedNumberFilter(
        field_name='angostura_sum_len', lookup_expr='gt',
        label='Angostura: ' + labels['sum_len']['gt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    angostura_sum_len__lt = GroupedNumberFilter(
        field_name='angostura_sum_len', lookup_expr='lt',
        label='Angostura: ' + labels['sum_len']['lt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    angostura_frac_len__gt = GroupedNumberFilter(
        field_name='angostura_frac_len', lookup_expr='gt',
        label='Angostura: ' + labels['frac_len']['gt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )
    angostura_frac_len__lt = GroupedNumberFilter(
        field_name='angostura_frac_len', lookup_expr='lt',
        label='Angostura: ' + labels['frac_len']['lt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )

    # Combined dry length filters
    combined_sum_len__gt = GroupedNumberFilter(
        field_name='combined_sum_len', lookup_expr='gt',
        label='Middle Rio Grande: ' + labels['sum_len']['gt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    combined_sum_len__lt = GroupedNumberFilter(
        field_name='combined_sum_len', lookup_expr='lt',
        label='Middle Rio Grande: ' + labels['sum_len']['lt'], 
        group=labels['sum_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['sum_len']['placeholder']})
    )
    combined_frac_len__gt = GroupedNumberFilter(
        field_name='combined_frac_len', lookup_expr='gt',
        label='Middle Rio Grande: ' + labels['frac_len']['gt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )
    combined_frac_len__lt = GroupedNumberFilter(
        field_name='combined_frac_len', lookup_expr='lt',
        label='Middle Rio Grande: ' + labels['frac_len']['lt'], 
        group=labels['frac_len']['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels['frac_len']['placeholder']})
    )


    class Meta:
        model = models.AllLen
        fields = [
            'dat__gt', 'dat__lt',
            'isleta_sum_len__gt', 'isleta_sum_len__lt', 'isleta_frac_len__gt', 'isleta_frac_len__lt',
            'acacia_sum_len__gt', 'acacia_sum_len__lt', 'acacia_frac_len__gt', 'acacia_frac_len__lt',
            'angostura_sum_len__gt', 'angostura_sum_len__lt', 'angostura_frac_len__gt', 'angostura_frac_len__lt',
            'combined_sum_len__gt', 'combined_sum_len__lt', 'combined_frac_len__gt', 'combined_frac_len__lt'
        ]

class DeltaDryFilter(django_filters.FilterSet):
    None
    # len = django_filters.NumberFilter()
    # len__gt = django_filters.NumberFilter(field_name='Len', lookup_expr='gt')
    # len__lt = django_filters.NumberFilter(field_name='Len', lookup_expr='lt')
    # # len = django_filters.RangeFilter()
    # # diff = django_filters.RangeFilter()
    # # diff = django_filters.RangeFilter()
    # class Meta:
    #     fields = ['...'] # , 'Diff', 'Domain', 'Date']

class DryCompFilter(django_filters.FilterSet):
    reach = django_filters.MultipleChoiceFilter(choices=models.Reach.objects.values_list('reach','reach'), )
    year = django_filters.NumberFilter()

    class Meta: 
        model = models.DryCompAgg
        fields = ['reach', 'year']

class SummaryUsgsFilter(GroupedFilterSetMixin, django_filters.FilterSet):
    field_lookup_label = ['usgs_id', 'choices', 'usgs_id']
    usgs_id = GroupedMultipleChoiceFilter(
        field_name=field_lookup_label[0], 
        label=labels[field_lookup_label[2]]['label'], 
        choices=models.UsgsFeatureGages.objects.values_list('usgs_id', 'usgs_feature_display_name'),
        group=labels[field_lookup_label[2]]['group'], 
          
    )

    # Define date filters
    field_lookup_label = ['dat', 'gt', 'dat']
    dat__gt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    field_lookup_label[1] = 'lt'
    dat__lt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    # Define flow filters
    field_lookup_label = ['flow_cfs', 'gt', 'flow_cfs']
    flow_cfs__gt = GroupedNumberFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    field_lookup_label[1] = 'lt'
    flow_cfs__lt = GroupedNumberFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    # provisional flag
    field_lookup_label = ['prov_flag', 'icontains', 'prov_flag']
    prov_flag = GroupedCharFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.TextInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
                                    )
    
    class Meta:
        model = models.UsgsFeatureData
        fields = ('dat__gt', 'dat__lt', 'flow_cfs__gt', 'flow_cfs__lt', 'prov_flag', 'usgs_id')

class DryLengthAggUsgsDataFilter(GroupedFilterSetMixin, django_filters.FilterSet):
    field_lookup_label = ['usgs_id', 'choices', 'usgs_id']
    usgs_id = GroupedMultipleChoiceFilter(
        field_name=field_lookup_label[0], 
        label=labels[field_lookup_label[2]]['label'], 
        choices=models.UsgsFeatureGages.objects.values_list('usgs_id', 'usgs_feature_display_name'),
        group=labels[field_lookup_label[2]]['group'], 
          
    )                                              
                                                    
    # Define date filters
    field_lookup_label = ['dat', 'gt', 'dat']
    dat__gt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    field_lookup_label[1] = 'lt'
    dat__lt = GroupedDateFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.DateInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    # Define flow filters
    field_lookup_label = ['flow_cfs', 'gt', 'flow_cfs']
    flow_cfs__gt = GroupedNumberFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    field_lookup_label[1] = 'lt'
    flow_cfs__lt = GroupedNumberFilter(
        field_name=field_lookup_label[0], 
        lookup_expr=field_lookup_label[1], 
        label=labels[field_lookup_label[2]][field_lookup_label[1]], 
        group=labels[field_lookup_label[2]]['group'], 
        widget=form_widgets.NumberInput(attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
    )

    # rms
    field_lookup_label = ['rm_down', 'gt', 'rm']
    rm_down__gt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[0] = 'rm_up'
    field_lookup_label[1] = 'lt'
    rm_up__lt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))

    # dry lengths
    field_lookup_label = ['dry_length', 'gt', 'dry_len']
    dry_length__gt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    field_lookup_label[1] = 'lt'
    dry_length__lt = GroupedNumberFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.NumberInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']}))
    
    # provisional flag
    field_lookup_label = ['prov_flag', 'icontains', 'prov_flag']
    prov_flag = GroupedCharFilter(field_name=field_lookup_label[0], lookup_expr=field_lookup_label[1], 
                                label=labels[field_lookup_label[2]][field_lookup_label[1]], 
                                group=labels[field_lookup_label[2]]['group'], 
                                widget=form_widgets.TextInput(
                                    attrs={'placeholder': labels[field_lookup_label[2]]['placeholder']})
                                    )
    

    class Meta:
        model = models.DryLengthAggUsgsData
        fields = ('dat__gt', 'dat__lt', "dry_length__gt", "dry_length__lt", "rm_down__gt", "rm_up__lt", 'flow_cfs__gt', 'flow_cfs__lt', 'prov_flag', 'usgs_id') 
