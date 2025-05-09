import shelve



if __name__ == '__main__':
    # python -m check_download_files 
    
    # jobposts/id_to_filename_db
    # jobposts/id_to_filename_remote_db
        
    with shelve.open('./jobposts/id_to_filename_remote_db') as db:
        id_to_filename = dict(db)
        print(len(id_to_filename))





