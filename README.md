# DjangoTube

Simple demo project for Django

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/abrahambrons/djangotube
   ```

2. Build and run the Docker containers:

   ```shell
   docker-compose up --build
   ```

   ```shell
   docker-compose up -d
   ```

3. Access the application at `http://localhost:8000`.

## Configuration

You can configure the application by modifying the environment variables in the `.env` file.

## Usage

### Common Use

To use the application, follow these steps:

1. Register for an account on the application.
2. Log in to your account.
3. Create a video using the nav menu after registering or creating a new account, you will need to create a channel first, but this is automatic, the app makes the redirection, you can use the url `/channels/create` to create a channel whatever you want
4. Browse and watch videos uploaded by other users using the index.
5. Like, comment videos.
6. You can see the popular videos in the `popular` view.
7. You can see your browsing history iun the `history` view.

## Development

- To run the Django development server:

  ```shell
  docker-compose run --rm web python manage.py runserver
  ```

- To run tests:

  ```shell
  docker-compose run --rm web python manage.py test
  ```

## Contributing

You can fork this project if you want

## License

Free distribution and use license MIT

## Acknowledgements

Django Project
