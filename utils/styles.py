class BillingStyles:
    FRAME_STYLE = "background-color: white; border: 2px solid #333;"
    TITLE_STYLE = "margin: 10px; padding: 10px; background-color: #333; color: white;"

    # cut the frame padding so buttons sit closer to the top/bottom
    CUSTOMER_FRAME_STYLE = """
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 0px;   /* was 10px */
        margin: 0;
    """

    # much less vertical padding / smaller margin
    CUSTOMER_BUTTON_STYLE = """
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #bbb;
            border-radius: 8px;
            padding: 6px 14px;
            margin: 4px;
            font-size: 13px;
            font-weight: 600;
            color: #333;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
        QPushButton:pressed {
            background-color: #dcdcdc;
        }
    """

    CUSTOMER_BUTTON_SELECTED_STYLE = """
        QPushButton {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QPushButton:pressed {
            background-color: #1e8449;
        }
    """


class KeypadStyles:
    NUMBER_STYLE = "background-color: #e0e0e0;"
    PLUS_MINUS_STYLE = "background-color: #ffa500; color: white;"
    CLEAR_STYLE = "background-color: #ff6b6b; color: white;"

class ActionButtonStyles:
    ADD_ROW_STYLE = "background-color: #2ecc71; color: white;"
    DELETE_ROW_STYLE = "background-color: #e74c3c; color: white;"
    PRICE_STYLE = "background-color: #3498db; color: white;"
    QTY_STYLE = "background-color: #9b59b6; color: white;"
    BILL_AMOUNT_STYLE = "color: #2c3e50; border: none; padding: 5px; font-weight: bold;"
    BILL_BUTTON_STYLE = """
        QPushButton {
            background-color: #2c3e50;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #34495e;
        }
        QPushButton:pressed {
            background-color: #1abc9c;
        }
    """


class CategoryStyles:
    FRAME_STYLE = "background-color: white; border: 1px solid #ddd;"
    TITLE_STYLE = """
        background-color: #333; 
        color: white; 
        padding: 10px; 
        margin-bottom: 5px;
    """
    BUTTON_STYLE = """
        QPushButton {
            background-color: #e8e8e8;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: left;
            padding: 10px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:pressed {
            background-color: #4CAF50;
            color: white;
        }
    """

class ProductStyles:
    FRAME_STYLE = "background-color: white; border: 1px solid #ddd;"
    TITLE_STYLE = """
        background-color: #333; 
        color: white; 
        padding: 10px; 
        margin-bottom: 5px;
    """
    BUTTON_STYLE = """
        QPushButton {
            background-color: #f9f9f9;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 11px;
            font-weight: bold;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
            border-color: #4CAF50;
        }
        QPushButton:pressed {
            background-color: #4CAF50;
            color: white;
        }
    """

class TitleBarStyles:
    TITLE_BAR_STYLE = """
            QWidget {
                background-color: #2c3e50;
                border-bottom: 2px solid #1abc9c;
            }
        """

    MENU_BUTTON_STYLE = """
        QPushButton {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.3);
        }
    """

    MINIMIZE_BUTTON_STYLE = """
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }
    """

    MAXIMIZE_BUTTON_STYLE = """
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }
    """

    CLOSE_BUTTON_STYLE = """
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #e74c3c;
        }
        QPushButton:pressed {
            background-color: #c0392b;
        }
    """

    MENU_STYLE = """
        QMenu {
            background-color: #2c3e50;
            border: 1px solid #34495e;
            border-radius: 8px;
            padding: 5px;
            color: white;
            font-size: 14px;
        }
        QMenu::item {
            background-color: transparent;
            padding: 8px 20px;
            border-radius: 4px;
            margin: 2px;
        }
        QMenu::item:selected {
            background-color: #1abc9c;
        }
        QMenu::separator {
            height: 1px;
            background-color: #34495e;
            margin: 5px 10px;
        }
    """

class GlobalStyles:
    GLOBAL_STYLE = """
        QWidget {
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 13px;
            
        }
        QPushButton {
            padding: 8px 14px;
            border: 1px solid #ccc;
            border-radius: 6px;
            background-color: #ffffff;
            color: #333;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #eef1f5;
            border-color: #999;
        }
        QPushButton:pressed {
            background-color: #d0d7df;
            border-color: #888;
        }
        QScrollArea {
            border: none;
        }
        QScrollBar:vertical, QScrollBar:horizontal {
            background: transparent;
        }
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background-color: #bbb;
            border-radius: 6px;
            min-height: 20px;
            min-width: 20px;
        }
        QScrollBar::handle:hover {
            background-color: #999;
        }
        QScrollBar::add-line, QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
    """


class ProductButtonStyles:
    BUTTON_STYLE = """
        QToolButton {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            font-size: 12px;
            font-weight: bold;
        }
        QToolButton:hover {
            background-color: #eaeaea;
        }
        QToolButton:pressed {
            background-color: #d6d6d6;
        }
    """


class MainContentStyles:
    FRAME_STYLE = "background-color: #f0f0f0; border: 1px solid #999;"

# Add these new style classes:

class CategoryButtonStyles:
    FRUITS_BUTTON_STYLE = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    """

    MANUAL_BUTTON_STYLE = """
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
    """

class BarcodeInputStyles:
    INPUT_STYLE = """
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
        }
        QLineEdit:focus {
            border-color: #2ecc71;
            background-color: #f9fffb;
        }
    """


class TitleLabelStyles:
    LABEL_STYLE = "color: white; padding: 5px;"