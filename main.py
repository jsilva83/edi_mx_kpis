# Include external packages.
from selenium import webdriver
import time
import constants
import main_functions as mf
import pandas as pd
# Import internal packages.
import dashboard_graph
# Constants.
PLAN_IO_QUERY_ALL_TASKS = 'https://seeburger.plan.io/projects/cu-21011-20210118/issues.csv?query_id=2056'
# Figure constants.
N_ROWS = 2
N_COLUMNS = 4
FIG_TITLE = 'EDI/MX Outlook Dashboard - '
FIG_SIZE_WIDTH = 16
FIG_SIZE_HEIGHT = 8
FIG_TITLE_COLOR = ['black']
# Bar color constants.
BAR_COLOR_BLUE = ['blue']
BAR_COLOR_WHITE = ['white']
BAR_COLOR_DOUBLE = ['red', 'blue']


def main():
    file_path = mf.get_user_downloads_folder() + '\\' + 'issues.csv'
    a_answer = input('Do you want to download issues file for MX from Seeburger? Enter {Y, N}: ').lower()
    if a_answer == 'y':
        # Open browser window.
        browser_window = webdriver.Chrome()
        browser_window.get('https://seeburger.plan.io/login?back_url=https%3A%2F%2Fseeburger.plan.io%2F')
        time.sleep(1)
        # Authenticate.
        mf.enter_credentials(browser_window, 5, 'jorge.silva@huf-group.com', 'YND5hdj.btq@rgc3mxc')
        mf.delete_file(file_path)  # if file exists, delete
        browser_window.get(PLAN_IO_QUERY_ALL_TASKS)  # download file issues.csv
        # Wait for file to download.
        time.sleep(2)
        # Close browser window.
        browser_window.quit()
    # Read file to dataframe.
    tasks_df = pd.read_csv(file_path)
    # Create data for the first graph => Communication setup (ALl Customers).
    # Filter dataframe for rows that are 'Customer' and 'Subject' contains 'Communication setup'.
    comm_setup_all_suppliers_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject'].str.contains('communication setup'))
    ]
    # Create a data series with column '% Done' just for the filtered rows.
    comm_setup_all_suppliers_ds = comm_setup_all_suppliers_df['% Done']
    # Calculate unique values counting.
    counting_percentages_comm_setup_ds = comm_setup_all_suppliers_ds.value_counts(ascending=True)
    # Add index 60 if it does not exist in the series index.
    if 60 not in counting_percentages_comm_setup_ds.index:
        counting_percentages_comm_setup_ds[60] = 0
    # Sort index to make sure it in ascending order.
    graph_1_ds = counting_percentages_comm_setup_ds.sort_index()
    # Axis 'X' values.
    graph_1_x = list(graph_1_ds.index)
    # Axis 'Y' values.
    graph_1_y = list(graph_1_ds.values)
    graph_1_avg = mf.calculate_average(graph_1_x, graph_1_y)
    # Create data for the second graph => Customer IN (All customers).
    costumer_in_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject'].str.contains('IN - mapping'))
    ]
    customer_in_ds = costumer_in_df['% Done']
    counting_percentages_customer_in_ds = customer_in_ds.value_counts(ascending=True)
    if 60 not in counting_percentages_customer_in_ds.index:
        counting_percentages_customer_in_ds[60] = 0
    graph_2_ds = counting_percentages_customer_in_ds.sort_index()
    graph_2_x = list(graph_2_ds.index)
    graph_2_y = graph_2_ds.values
    graph_2_avg = mf.calculate_average(graph_2_x, graph_2_y)
    # Create data for the third graph => Customer OUT (All customers).
    costumer_out_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject'].str.contains('OUT - mapping'))
    ]
    customer_out_ds = costumer_out_df['% Done']
    counting_percentages_customer_out_ds = customer_out_ds.value_counts(ascending=True)
    if 60 not in counting_percentages_customer_out_ds.index:
        counting_percentages_customer_out_ds[60] = 0
    graph_3_ds = counting_percentages_customer_out_ds.sort_index()
    graph_3_x = list(graph_3_ds.index)
    graph_3_y = graph_3_ds.values
    graph_3_avg = mf.calculate_average(graph_3_x, graph_3_y)
    # Create data for the fourth graph => Supplier IN (All suppliers).
    supplier_in_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Supplier') &
        (tasks_df['Subject'].str.contains('IN - mapping'))
    ]
    supplier_in_ds = supplier_in_df['% Done']
    counting_percentages_supplier_in_ds = supplier_in_ds.value_counts(ascending=True)
    if 60 not in counting_percentages_supplier_in_ds.index:
        counting_percentages_supplier_in_ds[60] = 0
    graph_4_ds = counting_percentages_supplier_in_ds.sort_index()
    graph_4_x = list(graph_4_ds.index)
    graph_4_y = graph_4_ds.values
    graph_4_avg = mf.calculate_average(graph_4_x, graph_4_y)
    # Create data for the fifth graph => Supplier OUT (All suppliers).
    supplier_out_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Supplier') &
        (tasks_df['Subject'].str.contains('OUT - mapping'))
        ]
    supplier_out_ds = supplier_out_df['% Done']
    counting_percentages_supplier_out_ds = supplier_out_ds.value_counts(ascending=True)
    if 60 not in counting_percentages_supplier_out_ds.index:
        counting_percentages_supplier_out_ds[60] = 0
    graph_5_ds = counting_percentages_supplier_out_ds.sort_index()
    graph_5_x = list(graph_5_ds.index)
    graph_5_y = graph_5_ds.values
    graph_5_avg = mf.calculate_average(graph_5_x, graph_5_y)
    # Create data for the sixth graph => Progress by customer (all costumers).
    customers_list = constants.PLAN_IO_QUERY_CUSTOMERS_MX
    customers_list.sort()
    # Prepare the output lists for graph 6.
    graph_6_x = customers_list
    graph_6_y = []
    # Transform the subject field into lowercase.
    tasks_df['Subject'] = tasks_df['Subject'].str.lower()
    # Cycle each customer item and calculate the average.
    for customer_item in customers_list:
        customer_item = customer_item.lower()
        customer_item_df = tasks_df[tasks_df['Subject'].str.contains(customer_item)]
        customer_item_ds = customer_item_df['% Done']
        average_progress = customer_item_ds.mean()
        graph_6_y.append(round(average_progress))
    graph_6_avg = round(sum(graph_6_y) / len(graph_6_y), 1)
    global_average = round((graph_1_avg + graph_2_avg + graph_3_avg + graph_4_avg + graph_5_avg) / 5, 1)
    # Start plotting.
    # Start creating the dashboard and its figure and axes.
    """Creates the figure and axes objects.\n
    in_n_rows: number of rows for axes grid.\n
    in_n_columns: number of columns for axes grid.\n
    in_fig_size_width: width of the figure.\n
    in_fig_size_height: height of the figure.\n
    in_fig_title: figure's title."""
    my_dashboard = dashboard_graph.DrawDashboard(
        in_n_rows=N_ROWS,
        in_n_columns=N_COLUMNS,
        in_fig_size_width=FIG_SIZE_WIDTH,
        in_fig_size_height=FIG_SIZE_HEIGHT,
        in_fig_title=FIG_TITLE,
        in_avg=global_average,
    )
    # Display graph in grid position (0, 0)
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
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[0],
        in_axe_title='MX Customers IN',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_2_x,
        in_x_rotation=0,
        in_y_legend='# customers',
        in_y_data=graph_2_y,
        in_inside_text=f'Average (in %): {graph_2_avg}',
        in_v_line_x=60,
        in_avg=graph_2_avg,
    )
    # Display graph in grid position (0, 1)
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[1],
        in_axe_title='MX Customers OUT',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_3_x,
        in_x_rotation=0,
        in_y_legend='# customers',
        in_y_data=graph_3_y,
        in_inside_text=f'Average (in %): {graph_3_avg}',
        in_v_line_x=60,
        in_avg=graph_3_avg,
    )
    # Display graph in grid position (0, 3)
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[2],
        in_axe_title='MX Suppliers IN',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_4_x,
        in_x_rotation=0,
        in_y_legend='# suppliers',
        in_y_data=graph_4_y,
        in_inside_text=f'Average (in %): {graph_4_avg}',
        in_v_line_x=60,
        in_avg=graph_4_avg,
    )
    # Display graph in grid position (0, 3)
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[3],
        in_axe_title='MX Suppliers OUT',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_5_x,
        in_x_rotation=0,
        in_y_legend='# suppliers',
        in_y_data=graph_5_y,
        in_inside_text=f'Average (in %): {graph_5_avg}',
        in_v_line_x=60,
        in_avg=graph_5_avg,
    )
    # Display graph in grid position (1, 0)
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[4],
        in_axe_title='Communications Setup (All)',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_1_x,
        in_x_rotation=0,
        in_y_legend='# channels',
        in_y_data=graph_1_y,
        in_inside_text=f'Average (in %): {graph_1_avg}',
        in_v_line_x=60,
        in_avg=graph_1_avg,
    )
    # Display graph in grid position (1, 1)
    my_dashboard.bar_graph(
        in_axe=my_dashboard.my_axes[5],
        in_axe_title='MX By Customers',
        in_bar_color=BAR_COLOR_DOUBLE,
        in_x_legend='customers',
        in_x_ticks_labels=graph_6_x,
        in_x_rotation=0,
        in_y_legend='progress (in %)',
        in_y_data=graph_6_y,
        in_inside_text=f'Average (in %): {graph_6_avg}'
    )
    # Add the traffic light to the image.
    my_dashboard.show_traffic_light(global_average)
    # Save dashboard.
    my_dashboard.save_image()
    # Show graphs.
    my_dashboard.show_graph()
    return


# Execute main function.
if __name__ == '__main__':
    main()
