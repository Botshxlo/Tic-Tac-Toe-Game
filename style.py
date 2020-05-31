# Botshelo Nokoane
# 2020/05/28
# style

import qstylizer.style  # install qstylzer usgin $ pip install qstlyzer

def styler():
    # Style the widgets on the main window
    css = qstylizer.style.StyleSheet()

    # style the Text Edit
    css.QTextEdit.setValues(
        borderRadius="7px",
        marginLeft = "2px",
        border="2px solid grey",
    )

    # style the Q labels
    css.QLabel.setValues(
        color = "black",
        marginLeft="6px"
    )

    # style the QWidget
    css.QWidget.setValues(
        backgroundColor="#5ce0c2",
        borderRadius="10px"
    )

    # style the connect button
    css.QPushButton.setValues(
        border="2px solid gray",
        paddingLeft="2px",
        paddingRight="2px"
    )

    # style the Line Edit
    css.QLineEdit.setValues(
        border="2px solid gray",
        paddingLeft="2px",
        paddingRight="2px"
    )

    # Style the tool button
    css.QToolButton.setValues(
        border="2px solid grey",
        marginLeft = "2px",
        marginRight = "2px",
        marginBottom = "2px",
        borderRadius="7px",
    )

    # change the push button style when pressed
    css.QPushButton.pressed.setValues(
        border="3px solid black",
        padding="5px",
        paddingLeft="-1px",
        marginRight="-1px",
        marginBottom="0px"
    )

    # change the tool button style when pressed
    css.QToolButton.pressed.setValues(
        border="3px solid black",
        padding="1px",
        marginLeft="5px",
        marginRight="5px",
        marginTop="5px",
        marginBottom="5px"
    )

    # change the tool button style when hovered
    css.QToolButton.hover.setValues(
        border="3px solid black"
    )

    # change the push button style when hovered
    css.QPushButton.hover.setValues(
        border="2px solid black"
    )

    # change the server line edit when its hovered
    css.QLineEdit.hover.setValues(
        border="2px solid black"
    )

    return css
