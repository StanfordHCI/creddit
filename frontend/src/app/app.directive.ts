import { Directive, EventEmitter, HostBinding, HostListener, Input, Output } from '@angular/core';

/**
 * Generated class for the LongPressDirective directive.
 *
 * See https://angular.io/docs/ts/latest/api/core/index/DirectiveMetadata-class.html
 * for more info on Angular Directives.
 */
@Directive({
  selector: '[long-press]'
})
export class LongPressDirective {

  private timeoutId: number = null;
  private intervalId: number = null;

  private isLongPressing: boolean;
  private isPressing: boolean;

  @Output() onLongPress = new EventEmitter();
  @Output() onLongPressing = new EventEmitter();

  @Input() timeout: number = 300;

  @HostBinding('class.press')
  get press() {
    return this.isPressing;
  }

  @HostBinding('class.long-press')
  get longPress() {
    return this.isLongPressing;
  }

  @HostListener('touchstart', ['$event'])
  public onMouseDown(event) {
    this.isPressing = true;
    this.isLongPressing = false;

    this.timeoutId = (<any> window).setTimeout(() => {
      this.isLongPressing = true;
      this.onLongPress.emit(event);

      this.intervalId = (<any> window).setInterval(() => {
        this.onLongPressing.emit(event);
      }, 30);
    }, this.timeout);
  }

  @HostListener('touchend', ['$event'])
  public onMouseLeave() {
    this.endPress();
  }

  private endPress() {
    if (this.timeoutId !== null)
      clearTimeout(this.timeoutId);

    if (this.intervalId !== null)
      clearInterval(this.intervalId);

    this.isLongPressing = false;
    this.isPressing = false;
  }

}
