import pygame
import sys


def show_message_box(title: str, message: str, width: int = 400, height: int = 200) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Microsoft YaHei", 24)
    btn_font = pygame.font.SysFont("Microsoft YaHei", 20)

    btn_rect = pygame.Rect(width // 2 - 40, height - 60, 80, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    running = False

        screen.fill((240, 240, 240))

        text_surf = font.render(message, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(width // 2, height // 2 - 20))
        screen.blit(text_surf, text_rect)

        mx, my = pygame.mouse.get_pos()
        btn_color = (100, 180, 100) if btn_rect.collidepoint(mx, my) else (80, 160, 80)
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=6)
        btn_text = btn_font.render("OK", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        screen.blit(btn_text, btn_text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    show_message_box("提示", "你好，这是 pygame 消息框!")
