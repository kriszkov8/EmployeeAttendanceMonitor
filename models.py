class User:
    def __init__(self, nume, prenume, companie, IdManager):
        self.nume = nume
        self.prenume = prenume
        self.companie = companie
        self.IdManager = IdManager

class Access:
    def __init__(self, ID_Persoana, data, sens, poarta):
        self.ID_Persoana = ID_Persoana
        self.data = data
        self.sens = sens
        self.poarta=poarta

