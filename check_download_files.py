import shelve



if __name__ == '__main__':
    # python -m check_download_files 
    
        
    with shelve.open('./jobposts/id_to_filename_db') as db:
        id_to_filename = dict(db)
        print(id_to_filename)





