# Include external packages.
from selenium import webdriver
import time
import main_functions as mf
import pandas as pd
# Constants.
PLAN_IO_QUERY_ALL_TASKS = 'https://seeburger.plan.io/projects/cu-21011-20210118/issues.csv?query_id=2056'


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
    # Create data for the first graph => Communication setup (ALl Customers)
    # Filter dataframe for rows that are 'Customer' and 'Subject' contains 'Communication setup'.
    comm_setup_all_suppliers_df = tasks_df[
        (tasks_df['Planio Label 1'] == 'Customer') &
        (tasks_df['Subject'].str.contains('communication setup'))
    ]
    # Create a data series with column '% Done' just for the filtered rows.
    comm_setup_all_suppliers_ds = comm_setup_all_suppliers_df['% Done']
    counting_percentages_ds = comm_setup_all_suppliers_ds.value_counts(ascending=True)
    graph_1_x = []
    graph_1_y = []
    for row in counting_percentages_ds.iteritems():
        graph_1_x.append(row[0])
        graph_1_y.append(row[1])
    return


# Execute main function.
if __name__ == '__main__':
    main()
