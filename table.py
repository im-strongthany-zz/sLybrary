from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    title = Col('Title')
    import_date = Col('Import Date')
    edit = LinkCol('Download', 'download', url_kwargs=dict(id='_id'))