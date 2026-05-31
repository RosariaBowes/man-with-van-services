# Man With Van Services South Wales Website

A full-stack business website developed for a removals and transport company operating across South Wales. The application provides customers with information about services, customer reviews, business contact details, and an administrative review management system.

The project was designed and deployed as a production-ready solution, combining responsive web design, backend development, database integration, and cloud deployment practices.

## Features

* Responsive design optimised for desktop, tablet, and mobile devices
* Customer review submission system
* Administrative review approval and moderation panel
* SQLite database integration for review storage
* Secure administrator authentication
* Dynamic content rendering using Flask
* Service showcase and image gallery
* Google Maps integration
* Search engine optimisation (SEO)
* XML sitemap generation and indexing
* Custom domain deployment with SSL certification
* Environment variable-based configuration management

## Technologies Used

### Backend

* Python
* Flask
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* CSS Media Queries

### Deployment & Development Tools

* Git
* GitHub
* Render
* Google Search Console

## Key Functionality

### Customer Review System

Customers can submit reviews directly through the website. Reviews are stored in a SQLite database and remain hidden until approved by an administrator.

### Admin Moderation Panel

A secure administration area allows authorised users to:

* Review customer submissions
* Approve reviews for public display
* Delete inappropriate or unwanted reviews
* Manage customer feedback

### Responsive Design

The website uses CSS media queries to provide a consistent user experience across a range of devices, including desktops, tablets, and smartphones.

### Search Engine Optimisation

SEO features include:

* XML sitemap generation
* Google Search Console integration
* Custom domain configuration
* Search engine indexing support

### Deployment

The application is deployed to a cloud hosting platform and configured with:

* Custom domain routing
* HTTPS / SSL certification
* Environment variable-based secret management
* Production-ready hosting infrastructure

## Security Considerations

To improve security and follow deployment best practices, sensitive configuration values are managed through environment variables rather than being stored directly within the source code.

This includes application secrets and administrative credentials used by the review management system.

## Installation

### Clone the Repository

```bash
git clone https://github.com/RosariaBowes/man-with-van-services.git
cd man-with-van-services
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file containing the required application configuration values and secrets.

### Run the Application

```bash
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

## Live Website

https://manwithvansouthwales.co.uk

## Future Improvements

Potential future enhancements include:

* Contact form email integration
* Online booking functionality
* Enhanced administration dashboard
* Cloud-hosted database migration
* Analytics and reporting features
* Additional SEO optimisation

## Author

Rosaria Bowes

GitHub: https://github.com/RosariaBowes
