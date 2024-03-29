
# Consider moving to something like sqlalchemy
class SimpleQueryBuilder:
    def __init__(self) -> None:
        self.query = ""
        self.where = []
        self.row_limit = ""
        self.row_skip = ""
        self.order_by_field = "id"
        self.args = []
        self.updates = []

    def update(self, table):
        self.query += f"UPDATE {table}"
        return self

    def select(self, table):
        self.query += f"SELECT * from {table}"
        return self
    
    def and_where(self, operator, *args):
        if len(self.where):
            self.where.append("AND")
        self.where.append(
            operator
        )
        self.args += args
        return self

    def limit(self, first):
        self.row_limit = f"limit {first}"

    def skip(self, skip):
        self.row_skip = f"OFFSET {skip}"

    def order_by(self, order_by, direction):
        self.order_by_field = order_by
        if direction:
            self.order_by_field += f" {direction}"

    def set_value_if_not_none(self, key, value):
        if value is not None:
            self.set_value(key, value)

    def set_value(self, key, value):
        if len(self.updates) > 0:
            self.updates.append(",\n")
        self.updates.append(f"{key} = \"{value}\"")

    def __str__(self):
        final_query = self.query
        if len(self.updates):
            final_query += "\nSET\n" 
            final_query += "".join(self.updates)

        if len(self.where):
            final_query += "\n WHERE " + "\n ".join(self.where)

        final_query += "\n"
        if len(self.updates) == 0:
            final_query += f"order by {self.order_by_field} NULLS LAST"

            if len(self.row_limit):
                final_query += "\n" 
                final_query += f"{self.row_limit}"
                final_query += "\n" 

            if len(self.row_skip):
                final_query += "\n" 
                final_query += f"{self.row_skip}"
                final_query += "\n" 

        return final_query

    def __repr__(self):
        return self.__str__()
