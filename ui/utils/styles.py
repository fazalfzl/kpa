# utils/styles.py (refactored with light futuristic theme)
from utils.constants import PRODUCT_BUTTON_FONT_SIZE


class ColorPalette:
    BASE_BG = "#e6f0fa"  # Softer blue background
    PRIMARY = "#007acc"  # Deeper blue (clear on all desktops)
    PRIMARY_DARK = "#005f99"  # Strong hover/active shade
    PRIMARY_LIGHT = "#b3dcf5"  # Noticeable light blue (visible on Lubuntu)
    ACCENT = "#f8f9fa"  # Soft off-white
    TEXT = "#0f172a"  # High-contrast dark blue-gray
    BORDER = "#94a3b8"  # Subtle border shade
    HOVER = "#dceaf7"  # Light blue hover
    PRESSED = "#bfdcf0"  # Click state


class ProductButtonStyles:
    BUTTON_STYLE = f"""
        QToolButton {{
            background-color: {ColorPalette.PRIMARY_LIGHT};
            border: 2px solid {ColorPalette.PRIMARY};
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
            font-size: {PRODUCT_BUTTON_FONT_SIZE}px;
            color: {ColorPalette.TEXT};
        }}
        QToolButton:hover {{
            background-color: {ColorPalette.HOVER};
        }}
        QToolButton:pressed {{
            background-color: {ColorPalette.PRIMARY};
            color: white;
        }}
    """




class GlobalStyles:
    GLOBAL_STYLE = f"""
        QWidget {{
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 13px;
            background-color: {ColorPalette.PRIMARY_LIGHT};
            color: {ColorPalette.TEXT};
        }}
        QPushButton {{
            padding: 8px 14px;
            border-radius: 8px;
            background-color: {ColorPalette.ACCENT};
            border: 1px solid {ColorPalette.BORDER};
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {ColorPalette.HOVER};
        }}
        QPushButton:pressed {{
            background-color: {ColorPalette.PRESSED};
        }}
        QScrollArea {{
            border: none;
        }}
        QScrollBar:vertical, QScrollBar:horizontal {{
            background: transparent;
            min-width: 50px;
        }}
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
            background-color: {ColorPalette.PRIMARY};
            border-radius: 6px;
            min-height: 20px;
            min-width: 20px;
        }}
        QScrollBar::handle:hover {{
            background-color: {ColorPalette.PRIMARY};
        }}
        QLineEdit, QTextEdit {{
            background-color: {ColorPalette.ACCENT};
            border: 1px solid {ColorPalette.BORDER};
            border-radius: 6px;
            padding: 6px;
            color: {ColorPalette.TEXT};
        }}
        QLineEdit:focus {{
            border-color: {ColorPalette.PRIMARY};
            background-color: {ColorPalette.HOVER};
        }}
    """


class BillingStyles:
    FRAME_STYLE = f"background-color: white; border: 2px solid {ColorPalette.BORDER};"
    TITLE_STYLE = f"margin: 10px; padding: 10px; background-color: {ColorPalette.PRIMARY}; color: white;"
    CUSTOMER_FRAME_STYLE = f"""
        background-color: {ColorPalette.ACCENT};
        border: 1px solid {ColorPalette.BORDER};
        padding: 0px;
        margin: 0;
    """
    CUSTOMER_BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE
    CUSTOMER_BUTTON_SELECTED_STYLE = f"""
        QPushButton {{
            background-color: {ColorPalette.PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {ColorPalette.PRIMARY_DARK};
        }}
        QPushButton:pressed {{
            background-color: #0369a1;
        }}
    """
    EDITING_BILL_LABEL_STYLE = f"""
        QLabel {{
            font-size: 14px;
            font-weight: bold;
            color: {ColorPalette.TEXT};
        }}
    """


class BillingListStyles:
    SCROLL_STYLE = f"QScrollArea {{ border: none; background-color: {ColorPalette.ACCENT}; }}"
    CONTAINER_STYLE = f"QWidget {{ background-color: {ColorPalette.ACCENT}; }}"


class BillingListItemStyles:
    SELECTED_STYLE = f"""
        QFrame {{
            border: 2px solid {ColorPalette.PRIMARY};
            border-radius: 4px;
            background-color: {ColorPalette.HOVER};
        }}
    """
    DEFAULT_STYLE = f"""
        QFrame {{
            border: 1px solid {ColorPalette.BORDER};
            border-radius: 4px;
            background-color: {ColorPalette.ACCENT};
        }}
        QFrame:hover {{
            background-color: {ColorPalette.HOVER};
        }}
    """
    COUNT_LABEL_STYLE = f"background-color: {ColorPalette.HOVER}; border-radius: 3px; padding: 2px 4px;"
    HIGHLIGHT_STYLE = f"color: {ColorPalette.TEXT}; background-color: {ColorPalette.PRIMARY_LIGHT}; border: 2px solid {ColorPalette.PRIMARY}; border-radius: 3px;"
    DEFAULT_FIELD_STYLE = f"color: {ColorPalette.TEXT}; background-color: {ColorPalette.ACCENT}; border: 1px solid {ColorPalette.BORDER}; border-radius: 3px;"


class BillingKeypadStyles:
    NUMBER_STYLE = f"background-color: {ColorPalette.HOVER}; color: {ColorPalette.TEXT};"
    PLUS_MINUS_STYLE = f"background-color: {ColorPalette.PRIMARY}; color: white;"
    CLEAR_STYLE = "background-color: #e11d48; color: white;"


class ActionButtonStyles:
    ADD_ROW_STYLE = "background-color: #10b981; color: white;"
    DELETE_ROW_STYLE = "background-color: #ef4444; color: white;"
    PRICE_STYLE = "background-color: #3b82f6; color: white;"
    QTY_STYLE = "background-color: #8b5cf6; color: white;"
    BILL_AMOUNT_STYLE = f"color: {ColorPalette.TEXT}; border: none; padding: 5px; font-weight: bold;"
    BILL_BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE


class CategoryStyles:
    FRAME_STYLE = f"background-color: {ColorPalette.ACCENT}; border: 1px solid {ColorPalette.BORDER};"
    TITLE_STYLE = f"background-color: {ColorPalette.PRIMARY}; color: white; padding: 10px; margin-bottom: 5px;"
    BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE


class ProductStyles:
    FRAME_STYLE = CategoryStyles.FRAME_STYLE
    TITLE_STYLE = CategoryStyles.TITLE_STYLE
    BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE


class TitleBarStyles:
    LAST_BILL_BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE
    TITLE_BAR_STYLE = f"QWidget {{ background-color: {ColorPalette.PRIMARY}; border-bottom: 2px solid {ColorPalette.PRIMARY_DARK}; }}"
    MENU_BUTTON_STYLE = GlobalStyles.GLOBAL_STYLE
    MINIMIZE_BUTTON_STYLE = MENU_BUTTON_STYLE
    MAXIMIZE_BUTTON_STYLE = MENU_BUTTON_STYLE
    CLOSE_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: transparent;
            border: none;
            color: {ColorPalette.TEXT};
            border-radius: 8px;
        }}
        QPushButton:hover {{
            background-color: #e74c3c;
        }}
        QPushButton:pressed {{
            background-color: #c0392b;
        }}
    """
    MENU_STYLE = f"""
        QMenu {{
            background-color: {ColorPalette.ACCENT};
            border: 1px solid {ColorPalette.BORDER};
            border-radius: 8px;
            padding: 5px;
            color: {ColorPalette.TEXT};
            font-size: 14px;
        }}
        QMenu::item {{
            background-color: transparent;
            padding: 8px 20px;
            border-radius: 4px;
            margin: 2px;
        }}
        QMenu::item:selected {{
            background-color: {ColorPalette.PRIMARY};
            color: white;
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {ColorPalette.BORDER};
            margin: 5px 10px;
        }}
    """





class MainContentStyles:
    FRAME_STYLE = f"background-color: {ColorPalette.HOVER}; border: 1px solid {ColorPalette.BORDER};"


class CategoryButtonStyles:
    FRUITS_BUTTON_STYLE = """
        QPushButton {
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #059669;
        }
        QPushButton:pressed {
            background-color: #047857;
        }
    """
    MANUAL_BUTTON_STYLE = """
        QPushButton {
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2563eb;
        }
        QPushButton:pressed {
            background-color: #1d4ed8;
        }
    """


class BarcodeInputStyles:
    INPUT_STYLE = f"""
        QLineEdit {{
            background-color: {ColorPalette.ACCENT};
            border: 1px solid {ColorPalette.BORDER};
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
            color: {ColorPalette.TEXT};
        }}
        QLineEdit:focus {{
            border-color: {ColorPalette.PRIMARY};
            background-color: {ColorPalette.HOVER};
        }}
    """


class TitleLabelStyles:
    LABEL_STYLE = f"color: {ColorPalette.TEXT}; padding: 5px;"
