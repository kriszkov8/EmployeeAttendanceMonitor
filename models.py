class User:
    def __init__(self, id, nume, prenume, companie, IdManager):
        self.id = id
        self.nume = nume
        self.prenume = prenume
        self.companie = companie
        self.IdManager = IdManager

class Acces:
    def __init__(self, id, data, ora, sens, id_user, id_poarta):
        self.id = id
        self.data = data
        self.ora = ora
        self.sens = sens
        self.id_user = id_user
        self.id_poarta = id_poarta

