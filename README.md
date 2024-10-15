# 💎 Poker Toolkit Project

## Poker Bankroll Manager

### Video Demo
[Watch the Poker Bankroll Manager Demo](https://youtu.be/GI0vrOjS7hU?si=RhnziVmrS3XnpVHw)

### Description
The **Poker Bankroll Manager** is a tool designed for poker players to track their bankroll and analyze their performance over time. The application allows the import of session data from CSV files and provides a detailed financial overview of sessions, including profit, hourly rate, session duration, and win rate. It also offers suggestions on improving financial strategies based on player performance.

#### Key Features:
- **CSV Data Import**: Players can import session data and filter sessions based on specific date ranges.
- **Overview of Sessions**: The tool calculates total sessions, profit, win rate, hourly rate, and provides advice based on results.
- **Graphical Reports**: Generates line and bar graphs to display monthly and total profits for easy visual analysis.
- **Customizable Reports**: Users can filter data by date and choose between different types of graphs to track their progress and financial results.

#### Technologies Used:
- **pandas** for data processing.
- **matplotlib** and **plotly** for generating visual reports.
- **tkinter** for building the graphical user interface (GUI).

The application aims to help poker players manage their bankroll, make informed financial decisions, and optimize their play by visualizing their results and offering strategic advice.

## Random Number Generator (RNG) Application

### Video Demo
[Watch the RNG Application Demo](https://www.youtube.com/watch?v=GI0vrOjS7hU&ab_channel=%C3%81rp%C3%A1dDemeter)

### Description
The **Random Number Generator (RNG) Application** is a simple tool designed to generate random numbers within a specified range. It's particularly useful for decision-making during poker games or other scenarios where randomness is needed. Users can define the range of numbers, and the application will generate a random number at an interval of 5 seconds. Additionally, users can manually generate a new random number by clicking a button.

#### Key Features:
- **Range Specification**: Users can input the minimum and maximum number for the random number range. The default range is 1 to 100.
- **Auto-Update**: The random number automatically updates every 5 seconds.
- **Manual Generation**: Users can click a button to generate a new random number at any time.
- **Graphical Interface**: Built using tkinter, the tool provides an intuitive and simple graphical user interface (GUI).

#### Technologies Used:
- **tkinter** for the GUI, allowing users to input number ranges and view the generated random number.
- **random** for generating random numbers within the user-specified range.
- **threading** to allow continuous number generation without interrupting the user's interaction.

This application is designed to help poker players or anyone who needs random number generation for decision-making, with automatic updates and manual options for flexibility.
