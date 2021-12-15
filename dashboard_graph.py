# Import external packages.
import matplotlib.pyplot as plot
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import numpy
import datetime
import os

# Global variables
FONT_TITLE = {'family': 'arial', 'color': 'black', 'size': 9}
FONT_XY_LABEL = {'family': 'arial', 'color': 'darkred', 'size': 8}
FONT_INSIDE_TEXT = {'family': 'arial', 'color': 'black', 'size': 8}
FONT_STACKED_BAR_LABEL = {'family': 'arial', 'color': 'black', 'size': 7}
FONT_TITLE_SIZE = 11
FONT_VALUE_LABEL_SIZE = 7
LABEL_SPACING = 3
PRIORITY_COLORS = ['red', 'orange', 'yellow', 'green']
PRIORITY_LABELS = ['critical', 'high', 'medium', 'low']


class DrawDashboard:

    def __init__(self, in_n_rows: int, in_n_columns: int, in_fig_size_width: int,
                 in_fig_size_height: int, in_fig_title: str, in_avg: float) -> None:
        """Creates the figure and axes objects.\n
        in_n_rows: number of rows for axes grid.\n
        in_n_columns: number of columns for axes grid.\n
        in_fig_size_width: width of the figure.\n
        in_fig_size_height: height of the figure."""
        # self.my_figure, self.my_axes = plot.subplots(
        #     nrows=in_n_rows,
        #     ncols=in_n_columns,
        #     figsize=(in_fig_size_width, in_fig_size_height)
        # )
        self.my_figure = plot.figure(figsize=(in_fig_size_width, in_fig_size_height))
        self.my_axes = []
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (0, 0)))
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (0, 1)))
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (0, 2)))
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (0, 3)))
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (1, 0)))
        self.my_axes.append(plot.subplot2grid((in_n_rows, in_n_columns), (1, 1), colspan=3))
        # Set figure's title.
        current_date = datetime.datetime.now()
        self.my_figure.suptitle(
            in_fig_title + current_date.strftime("%d.%m.%Y, %H:%M:%S") + ' - Total average: ' + str(in_avg) + '%',
            fontsize=FONT_TITLE_SIZE
        )
        self.my_figure.tight_layout(h_pad=3)
        return

    def bar_graph(self, in_axe: tuple, in_axe_title: str, in_bar_color: list,
                  in_x_legend: str, in_x_ticks_labels: list, in_x_rotation: int,
                  in_y_legend: str, in_y_data: list, in_inside_text) -> None:
        """Creates the elements to show in a bar graph.\n
        in_axe_index: index number (tuple) of the axes array to be used for the bar graph.\n
        in_axe_title: title of the graph (displayed on top).\n
        in_bar_color: color (str) or list of colors (list of str).\n
        in_x_legend: legend of the X axis (str).\n
        in_x_ticks_position: x positions (coordinates) on x ticks (tuple of int).\n
        in_x_ticks_labels: (list) labels to display on x ticks (list of str).\n
        in_x_rotation: (int) rotation angle of the x labels.\n
        in_y_legend: legend of the Y axis (str).\n
        in_y_data: the data for each bar (list)."""
        in_axe.set_title(in_axe_title, loc='center', fontdict=FONT_TITLE)
        in_axe.grid(axis='y', linestyle='dotted')
        in_axe.set_ylim(0, 100)
        # Axe X.
        in_axe.set_xlabel(in_x_legend, fontdict=FONT_XY_LABEL)
        x_ticks_position = numpy.arange(len(in_y_data))
        in_axe.set_xticks(x_ticks_position)
        in_axe.set_xticklabels(in_x_ticks_labels, fontsize=6, rotation=in_x_rotation)
        # Axe Y.
        in_axe.set_ylabel(in_y_legend, fontdict=FONT_XY_LABEL)
        in_axe.tick_params(axis='y', labelsize=6)
        in_axe.bar(x_ticks_position, in_y_data, align='center', color=in_bar_color, alpha=0.5)
        # Add label to each bar.
        self.add_values_to_labels(in_axe, in_y_data, in_spacing=LABEL_SPACING)
        # Write text inside the graph.
        in_axe.text(0.5, 0.9, in_inside_text,
                    FONT_INSIDE_TEXT,
                    horizontalalignment='center',
                    transform=in_axe.transAxes
                    )
        return

    def bar_graph_wit_v_line(self, in_axe: tuple, in_axe_title: str, in_bar_color: list, in_x_legend: str,
                             in_x_ticks_labels: list, in_x_rotation: int, in_y_legend: str, in_y_data: list,
                             in_inside_text: str, in_v_line_x: int, in_avg: float) -> None:
        """Creates the elements to show in a bar graph.\n
        in_axe_index: index number (tuple) of the axes array to be used for the bar graph.\n
        in_axe_title: title of the graph (displayed on top).\n
        in_bar_color: color (str) or list of colors (list of str).\n
        in_x_legend: legend of the X axis (str).\n
        in_x_ticks_position: x positions (coordinates) on x ticks (tuple of int).\n
        in_x_ticks_labels: (list) labels to display on x ticks (list of str).\n
        in_x_rotation: (int) rotation angle of the x labels.\n
        in_y_legend: legend of the Y axis (str).\n
        in_y_data: the data for each bar (list).\n
        in_inside_text: (str) the text to display at the center of the graph.
        in_v_line_x: (int) x coordinate to display a vertical line."""
        in_axe.set_title(in_axe_title, loc='center', fontdict=FONT_TITLE)
        in_axe.grid(axis='y', linestyle='dotted')
        # Axe X.
        in_axe.set_xlabel(in_x_legend, fontdict=FONT_XY_LABEL)
        x_ticks_position = numpy.arange(len(in_y_data))
        in_axe.set_xticks(x_ticks_position)
        in_axe.set_xticklabels(in_x_ticks_labels, fontsize=6, rotation=in_x_rotation)
        # Axe Y.
        in_axe.set_ylabel(in_y_legend, fontdict=FONT_XY_LABEL)
        in_axe.tick_params(axis='y', labelsize=6)
        in_axe.bar(x_ticks_position, in_y_data, align='center', color=in_bar_color, alpha=0.5)
        # Add label to each bar.
        self.add_values_to_labels(in_axe, in_y_data, in_spacing=LABEL_SPACING)
        # Write text inside the graph.
        in_axe.text(0.5, 0.9, in_inside_text, FONT_INSIDE_TEXT,
                    horizontalalignment='center',
                    transform=in_axe.transAxes
                    )
        # Create the vertical line.
        v_line_x_coordinate = in_x_ticks_labels.index(in_v_line_x)
        in_axe.vlines(
            v_line_x_coordinate,
            0, max(in_y_data),
            colors='r',
            linestyles='dotted',
            label=None,
        )
        # Add a traffic light to right upper corner.
        a_x = [len(in_x_ticks_labels) - 1]
        a_y = [max(in_y_data)]
        if in_avg < 60.00:
            in_axe.scatter(0.95, 0.95, color='#EE0202', s=120, transform=in_axe.transAxes)
        elif 100 > in_avg >= 60:
            in_axe.scatter(a_x, a_y, color='#EFF200', s=120, transform=in_axe.transAxes)
        else:
            in_axe.scatter(a_x, a_y, color='#00A301', s=120, transform=in_axe.transAxes)
        return

    @staticmethod
    def add_values_to_labels(in_axe, in_data, in_spacing) -> None:
        """Add labels to the end of each bar in a bar chart.
            Arguments:
                in_axe (matplotlib.axes.Axes): The matplotlib object containing the axes of the plot to annotate.
                in_data (list): list of data for each bar.
                in_spacing (int): The distance between the labels and the bars.
        """
        # 'index' is the index to get the label value.
        index = 0
        # For each bar: Place a label
        for rect in in_axe.patches:
            # Get X and Y placement of label from rectangle / bar.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            # Number of points between bar and label.
            space = in_spacing
            # Vertical alignment for positive values
            va = 'bottom'
            # If value of bar is negative: Place label below bar
            if y_value < 0:
                # Invert space to place label below
                space *= -1
                # Vertically align label at top
                va = 'top'
            # Use Y value as label and format number with one decimal place
            label = "{:.1f}".format(in_data[index])
            # Create annotation
            in_axe.annotate(
                label,  # Use `label` as label
                (x_value, y_value),  # Place label at end of the bar
                xytext=(0, in_spacing),  # Vertically shift label by `space`
                textcoords="offset points",  # Interpret `xytext` as offset in points
                ha='center',  # Horizontally center label
                va=va,  # Vertically align label differently for positive and negative values.
                fontfamily='arial',
                fontsize=FONT_VALUE_LABEL_SIZE,
                color='blue'
            )
            index += 1
        return

    @staticmethod
    def sum_int_list(in_int_list_1: list, in_int_list_2: list) -> list:
        out_sum_result = [sum(a_tuple) for a_tuple in list(zip(in_int_list_1, in_int_list_2))]
        return out_sum_result

    def stacked_bar_graph(self, in_axe_index: tuple, in_axe_title: str, in_bar_color: list,
                          in_x_legend: str, in_x_ticks_labels: list, in_x_rotation: str,
                          in_y_legend: str, in_y_data: list, in_stack_categories: list, in_inside_text) -> None:
        """Creates the elements to show in a bar graph.\n
        Arguments:
        in_axe_index: index number (tuple) of the axes array to be used for the bar graph.\n
        in_axe_title: title of the graph (displayed on top).\n
        in_bar_color: list of colors (list of str).\n
        in_x_legend: legend of the X axis (str).\n
        in_x_ticks_position: x positions (coordinates) on x ticks (tuple of int).\n
        in_x_ticks_labels: labels to display on x ticks (list of str).\n
        in_y_legend: legend of the Y axis (str).\n
        in_y_data: the data for each bar (list of lists).\n
        in_stack_categories: the categories to stack (1. Very High, 2. High, etc).\n
        in_inside_text: the text to insert inline with the graph."""
        g_row = in_axe_index[0]
        g_column = in_axe_index[1]
        self.my_axes[g_row][g_column].set_title(in_axe_title, loc='center', fontdict=FONT_TITLE)
        self.my_axes[g_row][g_column].grid(axis='y', linestyle='dotted')
        # Axe X.
        self.my_axes[g_row][g_column].set_xlabel(in_x_legend, fontdict=FONT_XY_LABEL)
        x_ticks_position = numpy.arange(len(in_y_data[0]))
        self.my_axes[g_row][g_column].set_xticks(x_ticks_position)
        self.my_axes[g_row][g_column].set_xticklabels(in_x_ticks_labels, fontsize=6, rotation=in_x_rotation)
        # Axe Y.
        self.my_axes[g_row][g_column].set_ylabel(in_y_legend, fontdict=FONT_XY_LABEL)
        self.my_axes[g_row][g_column].tick_params(axis='y', labelsize=6)
        # Baseline for first bar rect is 0.
        stack_len = len(in_y_data[0])
        bottom_coord = [[0 for _ in range(stack_len)], in_y_data[0]]
        for n in range(2, len(in_y_data)):
            sum_result = [0 for _ in range(stack_len)]
            for i in range(n):
                sum_result = self.sum_int_list(sum_result, in_y_data[i])
            bottom_coord.append(sum_result)
        # Create bar series (on per criticality).
        graph_bars = []
        for n in range(len(in_y_data)):
            graph_bars.append(self.my_axes[g_row][g_column].bar(x_ticks_position, in_y_data[n],
                                                                bottom=bottom_coord[n],
                                                                label=in_stack_categories[n],
                                                                align='center',
                                                                color=in_bar_color[n],
                                                                alpha=0.5
                                                                )
                              )
        # Write the labels inside the bars.
        for a_graph_bar in graph_bars:
            self.my_axes[g_row][g_column].bar_label(a_graph_bar,
                                                    label_type='center',
                                                    color='black',
                                                    fontsize=FONT_VALUE_LABEL_SIZE,
                                                    fontfamily='arial'
                                                    )
        # Write text inside the graph.
        self.my_axes[g_row][g_column].text(0.5, 0.9, in_inside_text,
                                           FONT_INSIDE_TEXT,
                                           horizontalalignment='center',
                                           transform=self.my_axes[in_axe_index].transAxes
                                           )
        # Show the legend
        self.my_axes[g_row][g_column].legend(fontsize=6)
        return

    def boxplot_bar_graph(self, in_axe_index: tuple, in_axe_title: str, in_bar_color: list,
                          in_x_legend: str, in_x_ticks_labels: list, in_x_rotation: str,
                          in_y_legend: str, in_y_data: list, in_inside_text: str, in_y_of_horizontal_lines=None
                          ) -> None:
        """Creates the elements to show in a bar graph.\n
        Arguments:
        in_axe_index: index number (tuple) of the axes array to be used for the bar graph.\n
        in_axe_title: title of the graph (displayed on top).\n
        in_bar_color: list of colors (list of str).\n
        in_x_legend: legend of the X axis (str).\n
        in_x_ticks_position: x positions (coordinates) on x ticks (tuple of int).\n
        in_x_ticks_labels: labels to display on x ticks (list of str).\n
        in_y_legend: legend of the Y axis (str).\n
        in_y_data: (list(list)) the data for each bar (list of lists).\n
        in_stack_categories: the categories to stack (1. Very High, 2. High, etc).\n
        in_inside_text: (str) the text to insert inline with the graph.\n
        in_y_of_horizontal_lines: (list) the y value for each horizontal line."""
        # Rectangular vertical box plot
        if in_y_of_horizontal_lines is None:
            in_y_of_horizontal_lines = []
        g_row = in_axe_index[0]
        g_column = in_axe_index[1]
        # Set graph title and y grid.
        self.my_axes[g_row][g_column].set_title(in_axe_title, loc='center', fontdict=FONT_TITLE)
        self.my_axes[g_row][g_column].grid(axis='y', linestyle='dotted')
        # Format dictionary the fliers data.
        red_outliers_props_dict = dict(markerfacecolor='red', marker='o', markeredgecolor='white', alpha=0.5)
        # Format dictionary for the box.
        box_props_dict = dict(color='black')
        # Format dictionary for the mean values.
        mean_props_dict = dict(marker=5, markerfacecolor='blue', markeredgecolor='blue', alpha=0.5)
        # Build the box plot from the data matrix.
        this_box_plot = self.my_axes[g_row][g_column].boxplot(in_y_data,
                                                              vert=True,  # vertical box alignment
                                                              patch_artist=True,  # fill with color
                                                              labels=in_x_ticks_labels,  # will be used to label x-ticks
                                                              showmeans=True,
                                                              flierprops=red_outliers_props_dict,
                                                              showfliers=True,
                                                              meanline=False,
                                                              boxprops=box_props_dict,
                                                              meanprops=mean_props_dict,
                                                              )
        # Color for each one of the boxes.
        for each_box_plot in this_box_plot['boxes']:
            each_box_plot.set_facecolor(in_bar_color[0])
            each_box_plot.set_alpha(0.5)
        # Write label in each mean symbol - triangle and calculate the total average.
        average_values_list = []
        for each_mean_in_plot in this_box_plot['means']:
            # Get the coordinates of the mean marker.
            x_value = each_mean_in_plot.get_xdata()
            y_value = each_mean_in_plot.get_ydata()
            # Add average value to calculate the total average.
            average_values_list.append(y_value)
            # The mean value is the Y value in the graph.
            mean_label_value = "{:.1f}".format(y_value[0])
            # Create annotation of the label next to the marker.
            self.my_axes[g_row][g_column].annotate(
                mean_label_value,  # Text of mean value.
                (x_value, y_value),  # Place label at end of the bar.
                xytext=(10, -3),  # Vertically shift label by 'space'.
                textcoords="offset points",  # Interpret 'xytext' as offset in points.
                ha='center',  # Horizontally center label.
                va='bottom',  # Vertically align label.
                fontfamily='arial',
                fontsize=FONT_VALUE_LABEL_SIZE,
                color='blue'  # Green color, to improve?!
            )
        # Calculate the total average value.
        total_average_value = sum(average_values_list) / len(average_values_list)
        # Axe X.
        self.my_axes[g_row][g_column].set_xlabel(in_x_legend, fontdict=FONT_XY_LABEL)
        self.my_axes[g_row][g_column].set_xticklabels(in_x_ticks_labels, fontsize=6, rotation=in_x_rotation)
        # Axe Y.
        self.my_axes[g_row][g_column].set_ylabel(in_y_legend, fontdict=FONT_XY_LABEL)
        self.my_axes[g_row][g_column].tick_params(axis='y', labelsize=6)
        # Draw the horizontal lines if the argument is not empty.
        if in_y_of_horizontal_lines is not None:
            for a_n in range(len(in_y_of_horizontal_lines)):
                a_y = in_y_of_horizontal_lines[a_n]
                self.my_axes[g_row][g_column].hlines(
                    a_y,
                    0, len(in_y_data),
                    colors=PRIORITY_COLORS[a_n],
                    linestyles='dotted',
                    label=PRIORITY_LABELS[a_n]
                )
        # Show the legend based in the horizontal lines labels.
        self.my_axes[g_row][g_column].legend(fontsize=6)
        # Write text inside the graph.
        if in_inside_text != '':
            self.my_axes[g_row][g_column].text(0.5, 0.9, in_inside_text,
                                               FONT_INSIDE_TEXT,
                                               horizontalalignment='center',
                                               transform=self.my_axes[in_axe_index].transAxes
                                               )
        else:
            a_text = f'Average (in hours): ' + '{:.1f}'.format(total_average_value[0])
            self.my_axes[g_row][g_column].text(0.5, 0.9, a_text,
                                               FONT_INSIDE_TEXT,
                                               horizontalalignment='center',
                                               transform=self.my_axes[in_axe_index].transAxes
                                               )
        return

    def make_axe_invisible(self, in_axe: tuple) -> None:
        # __init__
        g_row = in_axe[0]
        g_column = in_axe[1]
        # Set graph title and y grid.
        self.my_axes[g_row][g_column].set_visible(False)
        return

    def show_traffic_light(self, in_percentage) -> None:
        if in_percentage < 60:
            image_obj = plot.imread('./images/traffic-light-red-(100x100).png')
        elif 60 <= in_percentage < 90:
            image_obj = plot.imread('./images/traffic-light-yellow-(100x100).png')
        else:
            image_obj = plot.imread('./images/traffic-light-green-(100x100).png')
        # Arguments are x position followed by y position.
        self.my_figure.figimage(image_obj, 2200, 1500)
        return

    @staticmethod
    def show_graph() -> None:
        plot.tight_layout()
        plot.show()
        return

    @staticmethod
    def save_image() -> None:
        current_date = datetime.datetime.now()
        file_path = os.getenv('USERPROFILE') + '/Downloads/mx_edi_outlook_dashboard(' + \
                    current_date.strftime("%Y%m%d%H%M%S") + ').svg'
        plot.savefig(file_path, dpi=200, format='svg')
        return
