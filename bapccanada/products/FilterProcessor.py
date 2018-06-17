class FilterProcessor:
    def __init__(self, model, filter_dict):
        self.model = model
        self.filter_dict = filter_dict
        self.filtered_objects = self.model.objects.all()
        self.considered_filterable_dimensions = dict()
        self.considered_ratings = None
        self.ignored_filterable_dimensions = []
        self.filter_objects()

    def filter_objects(self):
        self.setup_filters()
        self.filter_by_measures()
        self.filter_by_ratings()
        self.filter_by_additional_dimensions()

    def setup_filters(self):
        for dimension in self.filter_dict.get('dimensions').items():
            for value in dimension[1]:
                filter_value = value.get('filter_value')
                value_selected = value.get('was_checked')
                filterable_dimension_name = value.get('filterable_dimension_name')

                if filterable_dimension_name not in self.ignored_filterable_dimensions:
                    if filter_value == 'ALL' and value_selected:
                        self.ignored_filterable_dimensions.append(filterable_dimension_name)
                    elif value_selected:
                        if filterable_dimension_name not in self.considered_filterable_dimensions.keys():
                            self.considered_filterable_dimensions[filterable_dimension_name] = [filter_value]
                        else:
                            self.considered_filterable_dimensions[filterable_dimension_name].append(filter_value)

        all_star_checked = False
        for rating in self.filter_dict.get('ratings').items():
            rating_object = rating[1]

            if rating_object.get('was_checked'):
                rating_threshold = rating_object.get('star_num')

                if rating_object.get('all_star'):
                    all_star_checked = True
                if not all_star_checked and (
                        self.considered_ratings is None or rating_threshold > self.considered_ratings):
                    self.considered_ratings = rating_threshold

    def filter_by_measures(self):
        price_range = self.filter_dict.get('ranges')
        max = price_range.get('max')
        min = price_range.get('min')
        selected_max = price_range.get('selected_max')
        selected_min = price_range.get('selected_min')

        if not min == selected_min:
            self.filtered_objects = self.filtered_objects.filter(cheapest_price__gte=selected_min)

        if not max == selected_max:
            self.filtered_objects = self.filtered_objects.filter(cheapest_price__lte=selected_max)

    def filter_by_ratings(self):
        if self.considered_ratings is not None:
            self.filtered_objects = self.filtered_objects.filter(average_rating__gte=self.considered_ratings)

    def filter_by_additional_dimensions(self):
        if len(self.considered_filterable_dimensions) is not 0:
            q_object_args = {}

            for filterable_dimension in self.considered_filterable_dimensions.items():
                filterable_values = filterable_dimension[1]
                filterable_parameter = filterable_dimension[0] + "__in"

                q_object_args[filterable_parameter] = filterable_values

            # dynamically unpack arguments to filter
            # {manufacturer__in : ["A", "B"], cores__in : [3, 4]}
            # translates to filter(manufacturer__in=["A","B"], cores__in=[3,4]) and so on
            self.filtered_objects = self.filtered_objects.filter(**q_object_args)

    def get_filtered_objects(self):
        return self.filtered_objects
