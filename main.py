# Include external packages.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import constants as kt
import main_functions as mf
import pandas as pd
import numpy as np
from numpy import mean
import os
# Import internal packages.
import dashboard_graph
import pptx_read as ppt
# Constants.
PLAN_IO_QUERY_ALL_TASKS = 'https://seeburger.plan.io/projects/cu-21011-20210118/issues.csv?query_id=2056'
SNP_STATUS_REPORT = 'C:/Users/jorge.silva/SNP Schneider-Neureither & Partner SE/SNP-O365-EXT-PRO-HUF_MEXICO - ' \
                    'Status Reports/27APR2022 - HUF Mexico EDI Status Dashboard.pptx'
# Figure constants.
N_ROWS = 3
N_COLUMNS = 4  # previously 3
FIG_TITLE = 'EDI/MX Outlook Dashboard - '
FIG_SIZE_WIDTH = 16  # previously 14
FIG_SIZE_HEIGHT = 10
FIG_TITLE_COLOR = ['black']
# Bar color constants.
BAR_COLOR_BLUE = ['blue']
BAR_COLOR_WHITE = ['white']
BAR_COLOR_DOUBLE = ['red', 'blue']


def main():

    file_path = mf.get_user_downloads_folder() + '\\' + 'issues.csv'
    a_answer = input('Do you want to download issues file for MX from Seeburger? Enter {Y, N}:\n').lower()

    if a_answer == 'y':

        # Check that file 'issues.csv' exist and delete it.
        if os.path.isfile(file_path):
            os.remove(file_path)

        # Check password.
        a_password = os.environ.get('SEEBURGER_PLANIO_PASSWORD')
        if a_password is None:
            a_password = input('Enter your password to Seeburger site:\n')

        # Open browser window.
        browser_window = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser_window.get('https://seeburger.plan.io/login?back_url=https%3A%2F%2Fseeburger.plan.io%2F')
        time.sleep(1)

        # Authenticate.
        mf.enter_credentials(browser_window, 5, 'jorge.silva@huf-group.com', a_password)
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
    # Version 1.0.
    # costumer_in_df = tasks_df[
    #     (tasks_df['Planio Label 1'] == 'Customer') &
    #     (tasks_df['Subject'].str.contains('IN - mapping'))
    # ]
    # Get the data that pertains to 'Customer' the subject contains 'IN - mapping' and status is different
    # from 'Removed (Closed)'
    costumer_in_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject'].str.contains('IN - mapping')) &
        (tasks_df['Status'] != 'Removed (Closed)') &
        (tasks_df['Status'] != 'Rejected (Closed)')
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
        (tasks_df['Subject'].str.contains('OUT - mapping')) &
        (tasks_df['Status'] != 'Removed (Closed)') &
        (tasks_df['Status'] != 'Rejected (Closed)')
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
    customers_list = kt.PLAN_IO_QUERY_CUSTOMERS_MX

    # customers_list.sort()
    # Prepare the output lists for graph 6.
    graph_6_x = customers_list
    graph_6_y = []

    # Transform the subject field into lowercase.
    tasks_df['Subject'] = tasks_df['Subject'].str.lower()

    # Cycle each customer item and calculate the average.
    for customer_item in customers_list:

        # Select rows that contain the customer name from an external list.
        customer_item = customer_item.lower()

        if customer_item == 'gm':

            # TODO: If customer is GM it enters in conflict with consignment word for TDK.
            customer_item_df = tasks_df[tasks_df['Subject'].str.contains(customer_item)]
            customer_item_df = customer_item_df[~(customer_item_df['Subject'].str.contains('tdk'))]

        else:

            customer_item_df = tasks_df[tasks_df['Subject'].str.contains(customer_item)]

        # From those, select rows that are no in the set {'Rejected (Closed)', 'Removed (Closed)'}.
        customer_item_df_1 = customer_item_df[~((customer_item_df['Status'] == 'Rejected (Closed)')
                                                | (customer_item_df['Status'] == 'Removed (Closed)'))]

        # Calculate the average of all pending and open tasks.
        customer_item_ds = customer_item_df_1['% Done']

        average_progress = customer_item_ds.mean()
        graph_6_y.append(round(average_progress))

    graph_6_avg = round(sum(graph_6_y) / len(graph_6_y), 1)

    # Calculate the global average.
    global_average = round((graph_1_avg + graph_2_avg + graph_3_avg + graph_4_avg + graph_5_avg) / 5, 1)

    # Read the ppt file and get the data.
    # Prepare the data to compute the 'Data Readiness' from SNP Status Report.
    a_pptx = ppt.PPTXRead(SNP_STATUS_REPORT)

    # Slide 1.
    a_pptx_table_dict_1 = a_pptx.get_table_values(in_slide_nr=0)

    # Table dictionary output:
    # {'Inbound/Outbound': {'SD-03': '6.6%', 'FI-02': '84.4%', 'FI-02': '93.9'}, 'Outbound': {'EWM-02': '0.0%'}}
    a_pptx_table_value_legend_1 = []
    a_pptx_table_x_1 = []
    a_pptx_table_y_1 = []
    a_colors_1 = []

    for (key1, value1) in a_pptx_table_dict_1.items():

        a_pptx_table_value_legend_1.append(key1)
        # Add number of items per color:
        a_colors_1.append(len(value1.keys()))

        for (key2, value2) in value1.items():
            a_pptx_table_x_1.append(key2)
            a_pptx_table_y_1.append(value2)

    # Calculate colors.
    a_pptx_table_colors_1 = []
    a_pptx_table_colors_1.extend('red' for _ in range(a_colors_1[0]))
    a_pptx_table_colors_1.extend('blue' for _ in range(a_colors_1[1]))

    # Slide 2.
    a_pptx_table_dict_2 = a_pptx.get_table_values(in_slide_nr=1)

    # Table dictionary output:
    # {'Inbound/Outbound': {'SD-03': '6.6%', 'FI-02': '84.4%', 'FI-02': '93.9'}, 'Outbound': {'EWM-02': '0.0%'}}
    a_pptx_table_value_legend_2 = []
    a_pptx_table_x_2 = []
    a_pptx_table_y_2 = []
    a_colors_2 = []

    for (key1, value1) in a_pptx_table_dict_2.items():

        a_pptx_table_value_legend_2.append(key1)
        # Add number of items per color:
        a_colors_2.append(len(value1.keys()))

        for (key2, value2) in value1.items():

            a_pptx_table_x_2.append(key2)
            a_pptx_table_y_2.append(value2)

    # Calculate colors.
    a_pptx_table_colors_2 = []
    a_pptx_table_colors_2.extend('red' for _ in range(a_colors_2[0]))
    a_pptx_table_colors_2.extend('blue' for _ in range(a_colors_2[1]))

    # ---------------------------------------------------------------------------------------------
    # Calculate the data for the graph: INBOUND customer counting of messages above 60% and bellow 60%.

    # Step 1: remove lines that are not related to customer, not inbound and were removed or rejected.
    tasks_df = pd.read_csv(file_path)
    df_1 = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject']).str.contains('IN - mapping') &
        (~tasks_df['Status'].isin(['Removed (Closed)', 'Rejected (Closed)', 'Wait (see comment)']))
    ]

    # Leave only the columns of interest.
    df_1 = df_1[['Subject', '% Done']]

    # Step 2: add a column with the customer name and remove non-critical customers.
    subject_lst = list(df_1['Subject'])
    customer_lst = [item.split('_')[0] for item in subject_lst]
    customer_lst = [item.split(' ')[0] for item in customer_lst]

    df_1.insert(1, 'Customer', customer_lst)
    df_1 = df_1.drop(columns=['Subject'])

    # Transform to lower case.
    plan_io_lower_customers = [item.lower() for item in kt.PLAN_IO_CRITICAL_CUSTOMERS_MX]
    df_1['Customer'] = df_1['Customer'].str.lower()
    df_2 = df_1[df_1['Customer'].isin(plan_io_lower_customers)]

    # ---------------------------------------------------------------------------------------------
    # Function to update the customer names in the dataframe but with only 6 chars.

    # Trim customer name to 6 chars.
    def trim_customer(row_value):

        if len(row_value) > 5:

            result = row_value[:5]

        else:

            result = row_value

        return result

    # Trim the column "Customer".
    df_2['Customer'] = df_2['Customer'].apply(trim_customer)

    # Step 3:
    # Rename column '% Done' to '60_done'
    df_2 = df_2.rename(columns={'% Done': '60_done'})

    # Duplicate column.
    df_2['40_done'] = df_2['60_done']

    # Update the value of column '40_done' with NaN if value is higher or equal to 60.
    df_2.loc[df_2['40_done'] >= 60, '40_done'] = np.nan
    df_2.loc[df_2['60_done'] < 60, '60_done'] = np.nan

    # Transform to lower case.
    df_2['Customer'] = df_2['Customer'].str.lower()

    # Count number of non NaN values.
    df_3 = df_2.groupby(by='Customer').count()

    # ---------------------------------------------------------------------------------------------
    # Calculate the data for the graph: OUTBOUND customer counting of messages above 60% and bellow 60%.

    # Step 1: remove lines that are not related to customer, not inbound and were removed or rejected.
    df_a = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject']).str.contains('OUT - mapping') &
        (~tasks_df['Status'].isin(['Removed (Closed)', 'Rejected (Closed)', 'Wait (see comment)']))
        ]

    # Leave only the columns of interest.
    df_a = df_a[['Subject', '% Done']]

    # Step 2: add a column with the customer name and remove non-critical customers.
    subject_lst = list(df_a['Subject'])
    customer_lst = [item.split('_')[0] for item in subject_lst]
    customer_lst = [item.split(' ')[0] for item in customer_lst]

    df_a.insert(1, 'Customer', customer_lst)
    df_a = df_a.drop(columns=['Subject'])

    # Transform to lower case.
    plan_io_lower_customers = [item.lower() for item in kt.PLAN_IO_CRITICAL_CUSTOMERS_MX]
    df_a['Customer'] = df_a['Customer'].str.lower()
    df_b = df_a[df_a['Customer'].isin(plan_io_lower_customers)]

    # Cut to the 6 chars on the left of the customer name.
    df_b['Customer'] = df_b['Customer'].apply(trim_customer)

    # Step 3:
    # Rename column '% Done' to '60_done'
    df_b = df_b.rename(columns={'% Done': '60_done'})

    # Duplicate column.
    df_b['40_done'] = df_b['60_done']

    # Update the value of column '40_done' with NaN if value is higher or equal to 60.
    df_b.loc[df_b['40_done'] >= 60, '40_done'] = np.nan
    df_b.loc[df_b['60_done'] < 60, '60_done'] = np.nan

    # Transform to lower case.
    df_b['Customer'] = df_b['Customer'].str.lower()

    # Count number of non NaN values.
    df_c = df_b.groupby(by='Customer').count()

    # ---------------------------------------------------------------------------------------------
    # Calculate the data for the graph: INBOUND Assignee (critical & <60%).

    # Step 1: remove lines that are not related to customer, not outbound and were removed or rejected.
    df_in_less_60 = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject']).str.contains('IN - mapping') &
        (tasks_df['Priority'] == 'High') &
        (~tasks_df['Status'].isin(['Removed (Closed)', 'Rejected (Closed)', 'Wait (see comment)']))
        ]

    # Step 2: keep only columns of interest and fill NaN with "NA, NA".
    df_in_less_60 = df_in_less_60[['Subject', 'Assignee', '% Done']]
    df_in_less_60.fillna('NA, NA', inplace=True)

    # Step 3: add a column with the customer name and remove non-critical customers.
    subject_lst = list(df_in_less_60['Subject'])
    customer_lst = [item.split('_')[0] for item in subject_lst]
    customer_lst = [item.split(' ')[0] for item in customer_lst]

    df_in_less_60.insert(1, 'Customer', customer_lst)
    df_in_less_60 = df_in_less_60.drop(columns=['Subject'])

    # Transform customers to lower case and filter those critical ones and bellow 60%.
    plan_io_lower_customers = [item.lower() for item in kt.PLAN_IO_CRITICAL_CUSTOMERS_MX]
    df_in_less_60['Customer'] = df_in_less_60['Customer'].str.lower()
    df_in_less_60 = df_in_less_60[df_in_less_60['Customer'].isin(plan_io_lower_customers)]
    df_in_less_60 = df_in_less_60[df_in_less_60['% Done'] < 60]

    # Leave only one name in the assignee field.
    # It might be that there is no "assignee" to tasks under 60% or length = 0.
    if df_in_less_60.shape[0] == 0:

        no_assignees_in_less_60 = True

    else:

        no_assignees_in_less_60 = False

        df_in_less_60['Assignee'] = df_in_less_60['Assignee'].str.split(pat=', ', expand=True)[1]
        # Count number of lines with grouped by assignee (use for graph).
        df_in_less_60_by_assignee = df_in_less_60.groupby(by='Assignee').count().sort_values('% Done', ascending=False)

    # ---------------------------------------------------------------------------------------------
    # Calculate the data for the graph: OUTBOUND Assignee (critical & <60%).

    # Step 1: remove lines that are not related to customer, not outbound and were removed or rejected.
    df_out_less_60 = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject']).str.contains('OUT - mapping') &
        (tasks_df['Priority'] == 'High') &
        (~tasks_df['Status'].isin(['Removed (Closed)', 'Rejected (Closed)', 'Wait (see comment)']))
        ]

    # Step 2: keep only columns of interest and fill NaN with "NA, NA".
    df_out_less_60 = df_out_less_60[['Subject', 'Assignee', '% Done']]
    df_out_less_60.fillna('NA, NA', inplace=True)

    # Step 3: add a column with the customer name and remove non-critical customers.
    subject_lst = list(df_out_less_60['Subject'])
    customer_lst = [item.split('_')[0] for item in subject_lst]
    customer_lst = [item.split(' ')[0] for item in customer_lst]

    df_out_less_60.insert(1, 'Customer', customer_lst)
    df_out_less_60 = df_out_less_60.drop(columns=['Subject'])

    # Transform customers to lower case and filter those critical ones and bellow 60%.
    plan_io_lower_customers = [item.lower() for item in kt.PLAN_IO_CRITICAL_CUSTOMERS_MX]
    df_out_less_60['Customer'] = df_out_less_60['Customer'].str.lower()
    df_out_less_60 = df_out_less_60[df_out_less_60['Customer'].isin(plan_io_lower_customers)]

    if df_out_less_60.shape[0] == 0:

        no_assignees_out_less_60 = True

    else:

        no_assignees_out_less_60 = False

        df_out_less_60 = df_out_less_60[df_out_less_60['% Done'] < 60]

        if df_out_less_60.shape[0] == 0:

            no_assignees_out_less_60 = True

        else:

            # Leave only one name in the assignee field.
            df_out_less_60['Assignee'] = df_out_less_60['Assignee'].str.split(pat=', ', expand=True)[1]

            # Count number of lines with grouped by assignee (use for graph).
            df_out_less_60_by_assignee = df_out_less_60.groupby(by='Assignee').count().sort_values('% Done', ascending=False)

    # ---------------------------------------------------------------------------------------------
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

    # Display graph in grid position (0, 0).
    # MX Customer IN.
    h60_indexes = [index for index, value in enumerate(graph_2_x) if value >= 60]
    sum_h60 = sum([value for index, value in enumerate(graph_2_y) if index in h60_indexes])
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[0],
        in_axe_title=f'MX Customers IN - Avg: {graph_2_avg}%',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_2_x,
        in_x_rotation=0,
        in_y_legend='# customers',
        in_y_data=graph_2_y,
        in_inside_text=f'Total msg: {sum_h60} / {sum(graph_2_y)}',
        in_v_line_x=60,
        in_avg=graph_2_avg,
    )

    # ---------------------------------------------------------------------------------------------
    # MX Customer IN (critical)
    # Position = (0, 1)

    my_dashboard.stacked_bar_graph(
        in_axe=my_dashboard.my_axes[1],
        in_axe_title='MX Customers IN (critical)',
        in_bar_color=['green', 'red'],
        in_x_legend='customers',
        in_x_ticks_labels=df_3.index,
        in_x_rotation='horizontal',
        in_y_legend='# messages',
        in_y_data=[list(df_3['60_done']), list(df_3['40_done'])],
        in_stack_categories=['>=60%', '<60%'],
        in_inside_text=f'{df_3["60_done"].sum()} out of {df_3["60_done"].sum() + df_3["40_done"].sum()}'
    )

    # ---------------------------------------------------------------------------------------------
    # Display graph in grid position (0, 2).

    # MX Customer OUT.
    h60_indexes = [index for index, value in enumerate(graph_3_x) if value >= 60]
    sum_h60 = sum([value for index, value in enumerate(graph_3_y) if index in h60_indexes])
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[2],
        in_axe_title=f'MX Customers OUT - Avg: {graph_3_avg}%',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_3_x,
        in_x_rotation=0,
        in_y_legend='# customers',
        in_y_data=graph_3_y,
        in_inside_text=f'Total msg: {sum_h60} / {sum(graph_3_y)}',
        in_v_line_x=60,
        in_avg=graph_3_avg,
    )

    # ---------------------------------------------------------------------------------------------
    # MX Customer OUT (critical)
    # Position = (0, 3)

    my_dashboard.stacked_bar_graph(
        in_axe=my_dashboard.my_axes[3],
        in_axe_title='MX Customers OUT (critical)',
        in_bar_color=['green', 'red'],
        in_x_legend='customers',
        in_x_ticks_labels=df_c.index,
        in_x_rotation='horizontal',
        in_y_legend='# messages',
        in_y_data=[list(df_c['60_done']), list(df_c['40_done'])],
        in_stack_categories=['>=60%', '<60%'],
        in_inside_text=f'{df_c["60_done"].sum()} out of {df_c["60_done"].sum() + df_c["40_done"].sum()}'
    )

    # Display graph in grid position (0, 3)
    # Communications Setup (All).
    # my_dashboard.bar_graph_wit_v_line(
    #     in_axe=my_dashboard.my_axes[3],
    #     in_axe_title=f'Communications Setup (All) - Avg: {graph_1_avg}%',
    #     in_bar_color=BAR_COLOR_BLUE,
    #     in_x_legend='progress (in %)',
    #     in_x_ticks_labels=graph_1_x,
    #     in_x_rotation=0,
    #     in_y_legend='# channels',
    #     in_y_data=graph_1_y,
    #     in_inside_text=f'',
    #     in_v_line_x=60,
    #     in_avg=graph_1_avg,
    # )

    # Display graph in grid position (1, 0).
    # MX Suppliers IN.
    h60_indexes = [index for index, value in enumerate(graph_4_x) if value >= 60]
    sum_h60 = sum([value for index, value in enumerate(graph_4_y) if index in h60_indexes])
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[4],
        in_axe_title=f'MX Suppliers IN - Avg: {graph_4_avg}%',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_4_x,
        in_x_rotation=0,
        in_y_legend='# suppliers',
        in_y_data=graph_4_y,
        in_inside_text=f'Total msg: {sum_h60} / {sum(graph_4_y)}',
        in_v_line_x=60,
        in_avg=graph_4_avg,
    )

    # Display graph in grid position (1, 1).
    # MX Suppliers OUT.
    h60_indexes = [index for index, value in enumerate(graph_5_x) if value >= 60]
    sum_h60 = sum([value for index, value in enumerate(graph_5_y) if index in h60_indexes])
    my_dashboard.bar_graph_wit_v_line(
        in_axe=my_dashboard.my_axes[5],
        in_axe_title=f'MX Suppliers OUT - Avg: {graph_5_avg}%',
        in_bar_color=BAR_COLOR_BLUE,
        in_x_legend='progress (in %)',
        in_x_ticks_labels=graph_5_x,
        in_x_rotation=0,
        in_y_legend='# suppliers',
        in_y_data=graph_5_y,
        in_inside_text=f'Total msg: {sum_h60} / {sum(graph_5_y)}',
        in_v_line_x=60,
        in_avg=graph_5_avg,
    )

    # ---------------------------------------------------------------------------------------------
    # Display graph in grid position (1, 2)

    # MX Data Readiness Customers.
    # my_dashboard.bar_graph(
    #     in_axe=my_dashboard.my_axes[6],
    #     in_axe_title=f'MX Data Readiness Customers - Avg: {round(mean(a_pptx_table_y_1), 2)}%',
    #     in_bar_color=a_pptx_table_colors_1,
    #     in_x_legend='objects',
    #     in_x_ticks_labels=a_pptx_table_x_1,
    #     in_x_rotation=45,
    #     in_y_legend='% complete',
    #     in_y_data=a_pptx_table_y_1,
    #     in_inside_text=f''
    # )

    # MX Assignee IN.
    if not no_assignees_in_less_60:

        my_dashboard.bar_graph(
            in_axe=my_dashboard.my_axes[6],
            in_axe_title=f'MX Assignee IN (critical & < 60%)',
            in_bar_color=BAR_COLOR_DOUBLE,
            in_x_legend='assignee',
            in_x_ticks_labels=df_in_less_60_by_assignee.index,
            in_x_rotation=0,
            in_y_legend='# tasks',
            in_y_data=df_in_less_60_by_assignee['% Done'],
            in_inside_text=f'',
            in_y_limits=(0, df_in_less_60_by_assignee['% Done'][0] + 1)
        )

    else:

        my_dashboard.make_axe_invisible(my_dashboard.my_axes[6])

    # ---------------------------------------------------------------------------------------------
    # Display graph in grid position (2, 0)

    # MX By Customers.
    a_bar_colors = []
    a_bar_colors.extend('red' for _ in range(12))
    a_bar_colors.extend('blue' for _ in range(9))

    my_dashboard.bar_graph(
        in_axe=my_dashboard.my_axes[8],
        in_axe_title=f'MX By Customers - Avg: {graph_6_avg}%',
        in_bar_color=a_bar_colors,
        in_x_legend='customers',
        in_x_ticks_labels=graph_6_x,
        in_x_rotation=0,
        in_y_legend='progress (in %)',
        in_y_data=graph_6_y,
        in_inside_text=f''
    )

    # ---------------------------------------------------------------------------------------------
    # Display graph in grid position (2, 2)

    # MX Data Readiness Suppliers.
    # my_dashboard.bar_graph(
    #     in_axe=my_dashboard.my_axes[9],
    #     in_axe_title=f'MMX Data Readiness Suppliers - Avg: {round(mean(a_pptx_table_y_2), 2)}%',
    #     in_bar_color=a_pptx_table_colors_2,
    #     in_x_legend='objects',
    #     in_x_ticks_labels=a_pptx_table_x_2,
    #     in_x_rotation=45,
    #     in_y_legend='% complete',
    #     in_y_data=a_pptx_table_y_2,
    #     in_inside_text=f''
    # )

    # MX Assignee OUT.
    if not no_assignees_out_less_60:

        my_dashboard.bar_graph(
            in_axe=my_dashboard.my_axes[9],
            in_axe_title=f'MX Assignee OUT (critical & < 60%)',
            in_bar_color=BAR_COLOR_DOUBLE,
            in_x_legend='assignee',
            in_x_ticks_labels=df_out_less_60_by_assignee.index,
            in_x_rotation=0,
            in_y_legend='# tasks',
            in_y_data=df_out_less_60_by_assignee['% Done'],
            in_inside_text=f'',
            in_y_limits=(0, df_out_less_60_by_assignee['% Done'][0] + 1)
        )

    else:

        my_dashboard.make_axe_invisible(my_dashboard.my_axes[9])

    # Add the traffic light to the image.
    my_dashboard.show_traffic_light(global_average)
    # Make some axes / graphs invisible.
    my_dashboard.make_axe_invisible(my_dashboard.my_axes[7])
    my_dashboard.make_axe_invisible(my_dashboard.my_axes[10])
    # Save dashboard.
    my_dashboard.save_image()
    # Show graphs.
    my_dashboard.show_graph()
    return


# Execute main function.
if __name__ == '__main__':
    main()
