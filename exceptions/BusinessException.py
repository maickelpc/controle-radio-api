class BusinessException(Exception):
    def __init__(self, message="Erro de negócio", errors=None):
        super().__init__(message)
        self.errors = errors  # Uma lista de erros associados, se houver
