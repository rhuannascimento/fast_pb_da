<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atividade 2</title>

    <style>

    body{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        row-gap: 2vh;
        height: 100vh;
    }

    </style>

</head>
<body>

    <h1>Escreva sua menssagaem</h1>

    <form action="process.php" method="POST">
        <input type="text" placeholder="Sua menssagem" name="message" id="message">
        <input type="submit" value="Enviar">
    </form>

    <span>Com Bind Mounts é possível atualizar o projeto em tempo real!</span>

</body>
</html>