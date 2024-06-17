from repository import communication_details_repo as cdr



def save_data_to_excel():

  df = cdr.get_data_repo()

  df.to_excel('test_comm.xlsx',index=False)