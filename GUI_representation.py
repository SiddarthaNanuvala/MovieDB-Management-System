import sys
import cx_Oracle
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt

# Database connection details
DB_USER = "SYSTEM"
DB_PASSWORD = "6174"
DB_DSN = "localhost:1521/xe"

class MovieDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disney+ Themed Movie Database")
        self.setGeometry(100, 100, 1000, 700)
        self.connection = None

        self.initUI()

    def initUI(self):
        """Setup the main user interface."""
        main_layout = QVBoxLayout()

        # Background Image Setup
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("C:\\Users\\codin\\OneDrive\\Desktop\\ESILV\\Subjects\\Advanced Data Base Management\\Project\\disney_background.jpg")
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Title Label
        self.title_label = QLabel("Welcome to Disney+ Movie Database", self)
        self.title_label.setFont(QFont("Arial", 30, QFont.Bold))
        self.title_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Centered Search Bar and Button Layout
        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignCenter)  # Centering the search bar and button

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by movie name, year, actor, or director")
        self.search_input.setStyleSheet("padding: 8px; font-size: 18px; background-color: #f2f2f2; border-radius: 5px;")
        self.search_input.setFixedHeight(40)
        
        self.search_button = QPushButton("Search", self)
        self.search_button.setStyleSheet("""
            background-color: #FF6F61;
            color: white;
            font-size: 18px;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.search_button.clicked.connect(self.search_movies)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        # Centered Query Section
        query_layout = QHBoxLayout()
        query_layout.setAlignment(Qt.AlignCenter)  # Centering the query section

        self.query_label = QLabel("Choose a Query:")
        self.query_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        self.query_combo = QComboBox()
        self.query_combo.addItems([
            "Show All Movies",
            "Show High-Rated Movies (IMDb > 9)",
            "Show Recently Added Movies",
            "Show Movies by Genre",
            "Show Movies by Director"
        ])
        self.query_combo.setStyleSheet("""
            font-size: 18px;
            padding: 8px;
            background-color: #f2f2f2;
            border-radius: 5px;
        """)

        self.run_query_button = QPushButton("Run Query")
        self.run_query_button.setStyleSheet("""
            background-color: #FF6F61;
            color: white;
            font-size: 18px;
            padding: 8px;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.run_query_button.clicked.connect(self.run_query)

        query_layout.addWidget(self.query_label)
        query_layout.addWidget(self.query_combo)
        query_layout.addWidget(self.run_query_button)
        main_layout.addLayout(query_layout)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setStyleSheet("""
            background-color: white; 
            alternate-background-color: #F2F2F2;
            font-size: 16px;
        """)
        self.results_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.results_table)

        # Additional Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.clear_button = QPushButton("Clear Table")
        self.clear_button.setStyleSheet("""
            background-color: #FF5733;
            color: white;
            font-size: 16px;
            padding: 8px;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.clear_button.clicked.connect(self.clear_table)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("""
            background-color: #900C3F;
            color: white;
            font-size: 16px;
            padding: 8px;
            font-weight: bold;
            border-radius: 5px;
        """)
        self.exit_button.clicked.connect(self.close_application)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.exit_button)
        main_layout.addLayout(button_layout)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def resizeEvent(self, event):
        """Override resize event to update background image."""
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        super().resizeEvent(event)

    def connect_db(self):
        """Connect to the Oracle database."""
        try:
            self.connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)
        except cx_Oracle.DatabaseError as e:
            QMessageBox.critical(self, "Error", f"Database Connection Failed: {e}")
            sys.exit(1)

    def run_query(self):
        """Run predefined queries."""
        query_type = self.query_combo.currentText()
        query = ""

        if query_type == "Show All Movies":
            query = "SELECT title, release_year, imdb_score FROM Titles"
        elif query_type == "Show High-Rated Movies (IMDb > 9)":
            query = "SELECT title, release_year, imdb_score FROM Titles WHERE imdb_score > 9"
        elif query_type == "Show Recently Added Movies":
            query = "SELECT title, release_year, imdb_score FROM Titles WHERE release_year >= EXTRACT(YEAR FROM SYSDATE) - 1"
        elif query_type == "Show Movies by Genre":
            query = "SELECT title, release_year, genres FROM Titles WHERE genres IS NOT NULL"
        elif query_type == "Show Movies by Director":
            query = "SELECT title, release_year, production_countries FROM Titles WHERE production_countries IS NOT NULL"

        self.execute_query(query)

    def search_movies(self):
        """Search for movies based on user input."""
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter a search term.")
            return

        query = f"""
        SELECT title, release_year, imdb_score 
        FROM Titles 
        WHERE LOWER(title) LIKE '%{search_text.lower()}%'
           OR release_year LIKE '%{search_text}%'
        """
        self.execute_query(query)

    def execute_query(self, query):
        """Execute a query and display results."""
        try:
            self.connect_db()
            cursor = self.connection.cursor()
            cursor.execute(query)

            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(len(columns))
            self.results_table.setHorizontalHeaderLabels(columns)

            for row_num, row_data in enumerate(results):
                self.results_table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    self.results_table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

            cursor.close()
        except cx_Oracle.DatabaseError as e:
            QMessageBox.critical(self, "Query Error", f"Error running query: {e}")
        finally:
            if self.connection:
                self.connection.close()

    def clear_table(self):
        """Clear the results table."""
        self.results_table.clearContents()
        self.results_table.setRowCount(0)

    def close_application(self):
        """Close the application."""
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieDatabaseApp()
    window.show()
    sys.exit(app.exec_())
