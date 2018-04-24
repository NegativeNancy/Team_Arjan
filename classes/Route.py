class Route():
    """Class that holds single route objects."""

    def __init__(self, connection_list):
        """Initialise class.""" 
        self.connection_list = connection_list

        self.time = 0
        for connection in self.connection_list:
            self.time += connection.time
