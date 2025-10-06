# CUKCU Django Project

A Django web application configured for deployment on Render with PostgreSQL database.

## Local Development Setup

1. **Clone the repository**

2. **Set up a virtual environment**
   ```
   python -m venv .cukcu
   .cukcu\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key-change-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/CUKCU
   ```

5. **Set up PostgreSQL database**
   - Install PostgreSQL if not already installed
   - Create a database named `CUKCU`
   ```
   CREATE DATABASE CUKCU;
   ```

6. **Run migrations**
   ```
   python manage.py migrate
   ```

7. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```
   python manage.py runserver
   ```

## Deployment on Render

1. **Push your code to a Git repository**

2. **Create a new Web Service on Render**
   - Connect your Git repository
   - Select "Python" as the environment
   - The build command and start command are already configured in `render.yaml`

3. **Set up PostgreSQL database on Render**
   - The database configuration is already set up in `render.yaml`
   - Render will automatically create a PostgreSQL database and link it to your web service

4. **Deploy your application**
   - Render will automatically deploy your application using the configuration in `render.yaml`
   - The first deployment may take a few minutes

5. **Run migrations on Render**
   - The migrations will be automatically run during the build process

6. **Create a superuser on Render**
   - After deployment, you can create a superuser using the Render shell

## Project Structure

- `CUKCU1/` - Main Django project directory
  - `settings/` - Settings module with base and production settings
- `cuckcuapp/` - Main application module
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
- `templates/` - HTML templates

## Google Search Visibility

To make your site visible on Google Search:

1. Create a `robots.txt` file in your static directory
2. Create a sitemap.xml file using Django's sitemap framework
3. Register your site with Google Search Console
4. Submit your sitemap to Google Search Console

## Additional Information

- The project uses Django 4.2 with PostgreSQL
- Static files are served using WhiteNoise
- Media files are stored locally in development and should be configured with a cloud storage service in production